from __future__ import annotations

from pydantic import BaseModel, Field


class ScanCreate(BaseModel):
    target: str | None = None


class DashboardStats(BaseModel):
    projects: int = 0
    assets: int = 0
    liveHosts: int = 0
    endpoints: int = 0
    jsFiles: int = 0
    apiSpecs: int = 0
    technologies: int = 0
    queueItems: int = 0
