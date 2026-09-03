from __future__ import annotations

from fastapi import APIRouter

from app.api.schemas.recon import DashboardStats
from app.api.services.project_service import service

router = APIRouter()


@router.get("/dashboard", response_model=DashboardStats)
def dashboard() -> dict:
    return service.get_dashboard_stats()
