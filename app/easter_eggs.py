"""Workshop extras for the FastAPI translation service.

Everything interesting in here is encoded on purpose. Yes, you could sit
down with `base64 -d` and crack it open in about thirty seconds -- but
where is the fun in that? Go poke at the running service instead. Start
with:

    curl http://localhost:8080/eggs
"""

from __future__ import annotations

import base64
import json
from functools import lru_cache

from fastapi.responses import PlainTextResponse

HINT_HEADER = "X-Easter-Eggs"

_VAULT = {
    "hint": (
        "MSBlZ2cgaGlkZGVuIGluIHRoaXMgc2VydmljZS4gU3RhcnQgd2l0aDogR0VUIC9lZ2dz"
    ),
    "greet": (
        "eyJQSVJBVEUiOiAiYWhveSB3b3JsZCwgeWUgc2N1cnZ5IGRldiEiLCAiTEVFVCI6ICJo"
        "M2xsMCB3MHJsZCIsICJFTU9KSSI6ICLwn5GLIPCfjI0iLCAiQklOQVJZIjogIjAxMTAx"
        "MDAwIDAxMTAxMDAxIn0="
    ),
    "riddle": (
        "8J+lmiBFYXN0ZXIgRWdnIEh1bnQgLSBGYXN0QVBJIFRyYW5zbGF0aW9uIFNlcnZpY2UK"
        "PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PQoK"
        "T25lIGVnZyBpcyBoaWRkZW4gaW4gdGhpcyBzZXJ2aWNlLgoKICAiVGhlIHRyYW5zbGF0"
        "aW9uIGZpbGUgaG9sZHMgODUgZ3JlZXRpbmdzLCBidXQgdGhlIHNlcnZpY2Uga25vd3MK"
        "ICAgYSBmZXcgaXQgbmV2ZXIgd3JvdGUgZG93bi4gUGlyYXRlcyBjYW4gcmVhZCB0aGVt"
        "LiIKCkhpbnQ6IG9uZSBlbnZpcm9ubWVudCB2YXJpYWJsZSBhbHJlYWR5IGRlY2lkZXMg"
        "d2hpY2ggZ3JlZXRpbmcgeW91CmdldCBiYWNrLCBhbmQgcmVzb3VyY2VzLyBpcyBub3Qg"
        "dGhlIG9ubHkgcGxhY2UgYSBncmVldGluZyBjYW4gbGl2ZS4KCkdvb2QgbHVjay4g8J+Q"
        "owo="
    ),
    "found": (
        "CgogICAgICAgICBfX19fX19fX19fXwogICAgICAgICcuXz09Xz09Xz1fLicKICAgICAg"
        "ICAuLVw6ICAgICAgLy0uCiAgICAgICB8ICh8Oi4gICAgIHwpIHwKICAgICAgICAnLXw6"
        "LiAgICAgfC0nCiAgICAgICAgICBcOjouICAgIC8KICAgICAgICAgICAnOjouIC4nCiAg"
        "ICAgICAgICAgICApICgKICAgICAgICAgICBfLicgJy5fCiAgICAgICAgICBgIiIiIiIi"
        "ImAKCvCfj4YgRUdHIEZPVU5EISDwn4+GCgpZb3UgdGF1Z2h0IHRoaXMgc2VydmljZSB0"
        "byBzcGVhayBhIGxhbmd1YWdlIHRoYXQgd2FzIG5ldmVyIGluCnJlc291cmNlcy90cmFu"
        "c2xhdGlvbnMuanNvbi4gR28gdGVsbCB0aGUgd29ya3Nob3AgZmFjaWxpdGF0b3IuIPCf"
        "kKM="
    ),
}


@lru_cache()
def _unwrap(key: str) -> str:
    return base64.b64decode(_VAULT[key]).decode("utf-8")


HINT_MESSAGE = _unwrap("hint")


def alternate_greeting(language: str) -> str | None:
    """A greeting the translation file has never heard of, if there is one."""
    return json.loads(_unwrap("greet")).get(language.upper())


def claim() -> str:
    """The 'you found it' banner, appended to the greeting."""
    return _unwrap("found")


def add_hint(response: PlainTextResponse) -> PlainTextResponse:
    """Nudge the curious toward the hunt without changing the body."""
    response.headers[HINT_HEADER] = HINT_MESSAGE
    return response


def eggs() -> PlainTextResponse:
    """Serves the riddle to anyone who asks."""
    return PlainTextResponse(_unwrap("riddle"))
