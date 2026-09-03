from __future__ import annotations

import ipaddress
import re
from urllib.parse import urlsplit

from pydantic import BaseModel, Field
from pydantic import field_validator


def normalize_target(value: str) -> str:
    target = value.strip()
    if not target:
        raise ValueError("Target is required")

    parsed = urlsplit(target if "://" in target else f"//{target}")
    if parsed.scheme and parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Target must be a domain, URL, or IP address")
    if parsed.hostname is None:
        raise ValueError("Target must be a domain, URL, or IP address")

    hostname = parsed.hostname.rstrip(".").lower()
    try:
        ipaddress.ip_address(hostname)
    except ValueError:
        if len(hostname) > 253 or not re.fullmatch(
            r"[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?", hostname
        ):
            raise ValueError("Target must be a domain, URL, or IP address") from None

    port = f":{parsed.port}" if parsed.port is not None else ""
    return f"{hostname}{port}"


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1)
    rootDomain: str = Field(..., min_length=1)
    description: str | None = None

    @field_validator("name", "description", mode="before")
    @classmethod
    def strip_text(cls, value: str | None) -> str | None:
        return value.strip() if isinstance(value, str) else value

    @field_validator("rootDomain", mode="before")
    @classmethod
    def validate_target(cls, value: str) -> str:
        return normalize_target(value)


class Project(BaseModel):
    id: str
    name: str
    rootDomain: str
    description: str | None = None
    status: str = "active"
    assetCount: int = 0
    endpointCount: int = 0
    lastScanAt: str | None = None
    createdAt: str
