from __future__ import annotations

import json
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from . import easter_eggs
from .config import AppConfig, load_config

ERROR_INVALID_JSON = "Invalid JSON format in {filename}"
ERROR_MISSING_FILE = "Could not find {filename} in resources."


def create_app(config: AppConfig | None = None) -> FastAPI:
    cfg = config or load_config()
    application = FastAPI()

    @application.get("/", response_class=PlainTextResponse)
    def read_root() -> PlainTextResponse:
        try:
            payload = cfg.translation_file_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return PlainTextResponse(
                ERROR_MISSING_FILE.format(filename=cfg.translation_file_name),
                status_code=500,
            )

        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            return PlainTextResponse(
                ERROR_INVALID_JSON.format(filename=cfg.translation_file_name),
                status_code=500,
            )

        translations = data.get("translations") if isinstance(data, dict) else None
        if not isinstance(translations, dict):
            return PlainTextResponse(
                ERROR_INVALID_JSON.format(filename=cfg.translation_file_name),
                status_code=500,
            )

        secret = easter_eggs.alternate_greeting(cfg.default_language)
        translation = (
            secret or translations.get(cfg.default_language) or translations.get("EN")
        )
        if not isinstance(translation, str):
            return PlainTextResponse(
                ERROR_INVALID_JSON.format(filename=cfg.translation_file_name),
                status_code=500,
            )

        timestamp = datetime.now(timezone.utc).isoformat()
        body = f"{translation} @ {timestamp}"
        if secret:
            body += easter_eggs.claim()

        return easter_eggs.add_hint(PlainTextResponse(body))

    @application.get("/eggs", response_class=PlainTextResponse)
    def read_eggs() -> PlainTextResponse:
        return easter_eggs.eggs()

    return application


app = create_app()


if __name__ == "__main__":
    from uvicorn import run

    cfg = load_config()
    run(
        app,
        host="0.0.0.0",
        port=cfg.port,
        reload=False,
    )
