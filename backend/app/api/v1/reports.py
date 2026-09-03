from __future__ import annotations

from fastapi import APIRouter

from app.api.services.project_service import service

router = APIRouter()


@router.get("/apis", response_model=list[dict])
def list_api_specs() -> list[dict]:
    return service.list_api_specs()


@router.get("/projects/{project_id}/apis", response_model=list[dict])
def list_project_api_specs(project_id: str) -> list[dict]:
    return service.list_api_specs(project_id)


@router.get("/technologies", response_model=list[dict])
def list_technologies() -> list[dict]:
    return service.list_technologies()


@router.get("/projects/{project_id}/technologies", response_model=list[dict])
def list_project_technologies(project_id: str) -> list[dict]:
    return service.list_technologies(project_id)


@router.get("/testing-queue", response_model=list[dict])
def list_queue_items() -> list[dict]:
    return service.list_queue_items()


@router.get("/projects/{project_id}/testing-queue", response_model=list[dict])
def list_project_queue_items(project_id: str) -> list[dict]:
    return service.list_queue_items(project_id)
