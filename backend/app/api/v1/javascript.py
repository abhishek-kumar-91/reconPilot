from __future__ import annotations

from fastapi import APIRouter

from app.api.services.project_service import service

router = APIRouter()


@router.get("/projects/{project_id}/javascript", response_model=list[dict])
def list_javascript(project_id: str) -> list[dict]:
    return service.list_javascript_files(project_id)


@router.get("/javascript", response_model=list[dict])
def list_all_javascript() -> list[dict]:
    return service.list_javascript_files()
