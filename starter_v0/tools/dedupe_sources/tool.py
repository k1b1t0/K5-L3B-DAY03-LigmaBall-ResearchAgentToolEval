from __future__ import annotations

from collections.abc import Mapping
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from tools._shared import err


_TRACKING_KEYS = {"fbclid", "gclid", "mc_cid", "mc_eid"}


def _canonical_url(url: str) -> str:
    parsed = urlsplit(url.strip())
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.hostname:
        raise ValueError(f"Invalid http(s) URL: {url!r}")

    host = parsed.hostname.lower()
    if host.startswith("www."):
        host = host[4:]
    port = parsed.port
    netloc = host if port is None or (parsed.scheme.lower(), port) in {("http", 80), ("https", 443)} else f"{host}:{port}"
    query = [
        (key, value)
        for key, value in parse_qsl(parsed.query, keep_blank_values=True)
        if not key.lower().startswith("utm_") and key.lower() not in _TRACKING_KEYS
    ]
    path = parsed.path.rstrip("/") or "/"
    return urlunsplit((parsed.scheme.lower(), netloc, path, urlencode(sorted(query)), ""))


def dedupe_sources(items: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Remove duplicate research items by normalized URL, preserving first occurrence."""
    try:
        if not isinstance(items, list):
            raise ValueError("items must be a list of objects")

        unique: list[dict[str, Any]] = []
        seen: set[str] = set()
        for index, item in enumerate(items):
            if not isinstance(item, Mapping):
                raise ValueError(f"items[{index}] must be an object")
            url = item.get("url")
            if not isinstance(url, str) or not url.strip():
                raise ValueError(f"items[{index}].url must be a non-empty URL")
            key = _canonical_url(url)
            if key not in seen:
                seen.add(key)
                unique.append(dict(item))

        return {
            "tool": "dedupe_sources",
            "items": unique,
            "input_count": len(items),
            "item_count": len(unique),
            "duplicates_removed": len(items) - len(unique),
        }
    except Exception as exc:
        return err("dedupe_sources", exc)
