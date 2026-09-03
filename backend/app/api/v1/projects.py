from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.api.schemas.project import Project, ProjectCreate
from app.api.schemas.recon import ScanCreate
from app.api.services.project_service import service

router = APIRouter()


@router.get("", response_model=list[Project])
def list_projects() -> list[dict]:
    return service.list_projects()


@router.post("", response_model=Project)
def create_project(payload: ProjectCreate) -> dict:
    project = service.create_project(payload.model_dump())
    return project


@router.get("/{project_id}", response_model=Project)
def get_project(project_id: str) -> dict:
    project = service.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.delete("/{project_id}")
def delete_project(project_id: str) -> dict[str, str]:
    if not service.delete_project(project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted", "id": project_id}


@router.post("/{project_id}/scan")
def start_project_scan(project_id: str, payload: ScanCreate | None = None) -> dict:
    project = service.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return service.start_scan(project_id, payload.target if payload and payload.target else project["rootDomain"])
