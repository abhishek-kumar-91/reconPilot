from __future__ import annotations

from fastapi import APIRouter

from app.api.services.project_service import service

router = APIRouter()


@router.get("/projects/{project_id}/endpoints", response_model=list[dict])
def list_endpoints(project_id: str) -> list[dict]:
    return service.list_endpoints(project_id)


@router.get("/endpoints", response_model=list[dict])
def list_all_endpoints() -> list[dict]:
    return service.list_endpoints()
