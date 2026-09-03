from __future__ import annotations

from fastapi import APIRouter, HTTPException

router = APIRouter()

from app.api.schemas.recon import ScanCreate
from app.api.services.project_service import service


@router.get("/scans", response_model=list[dict])
def list_scans() -> list[dict]:
    return service.list_scans()


@router.get("/projects/{project_id}/scans", response_model=list[dict])
def list_project_scans(project_id: str) -> list[dict]:
    scans = service.list_scans(project_id)
    return scans


@router.get("/scans/{scan_id}", response_model=dict)
def get_scan(scan_id: str) -> dict:
    scan = service.get_scan(scan_id)
    if scan is None:
        raise HTTPException(status_code=404, detail="Scan not found")
    return scan


@router.post("/projects/{project_id}/scans")
def create_scan(project_id: str, payload: ScanCreate | None = None) -> dict:
    project = service.get_project(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return service.start_scan(project_id, payload.target if payload and payload.target else project["rootDomain"])
