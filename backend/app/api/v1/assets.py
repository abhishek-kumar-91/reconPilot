from __future__ import annotations

from fastapi import APIRouter

from app.api.services.project_service import service

router = APIRouter()


@router.get("/projects/{project_id}/assets", response_model=list[dict])
def list_assets(project_id: str) -> list[dict]:
    return service.list_assets(project_id)


@router.get("/assets", response_model=list[dict])
def list_all_assets() -> list[dict]:
    return service.list_assets()
