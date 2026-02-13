from __future__ import annotations

import re

_MAX_NAME_LENGTH = 128
_NAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 .,'_-]*$")


def _normalize_whitespace(value: str) -> str:
    return " ".join(value.strip().split())


def normalize_lgu(lgu: str) -> str:
    normalized = _normalize_whitespace(lgu)
    if not normalized:
        raise ValueError("LGU cannot be empty.")
    if len(normalized) > _MAX_NAME_LENGTH:
        raise ValueError("LGU is too long.")
    if not _NAME_PATTERN.match(normalized):
        raise ValueError("LGU contains unsupported characters.")
    return normalized


def normalize_crop(crop: str) -> str:
    normalized = _normalize_whitespace(crop)
    if not normalized:
        raise ValueError("Crop cannot be empty.")
    if len(normalized) > _MAX_NAME_LENGTH:
        raise ValueError("Crop name is too long.")
    if not _NAME_PATTERN.match(normalized):
        raise ValueError("Crop contains unsupported characters.")
    return normalized.title()
