from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
RESOURCES_DIR = BASE_DIR / "resources"


@dataclass(frozen=True)
class AppConfig:
    default_language: str
    translation_file_name: str
    translation_file_path: Path
    port: int


def _read_port(value: str | None) -> int:
    try:
        return int(value) if value else 8080
    except (TypeError, ValueError):
        return 8080


def load_config() -> AppConfig:
    default_language = os.environ.get("TRANSLATION_DEFAULT_LANGUAGE", "EN").upper()
    translation_file_name = os.environ.get("TRANSLATION_FILE", "translations.json")
    translation_file_path = RESOURCES_DIR / translation_file_name
    port = _read_port(os.environ.get("PORT"))

    return AppConfig(
        default_language=default_language,
        translation_file_name=translation_file_name,
        translation_file_path=translation_file_path,
        port=port,
    )
