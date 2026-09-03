from fastapi import APIRouter

from app.api.v1.assets import router as assets_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.endpoints import router as endpoints_router
from app.api.v1.javascript import router as javascript_router
from app.api.v1.projects import router as projects_router
from app.api.v1.reports import router as reports_router
from app.api.v1.scans import router as scans_router

api_router = APIRouter()

api_router.include_router(projects_router, prefix="/projects", tags=["projects"])
api_router.include_router(scans_router, tags=["scans"])
api_router.include_router(assets_router, tags=["assets"])
api_router.include_router(endpoints_router, tags=["endpoints"])
api_router.include_router(javascript_router, tags=["javascript"])
api_router.include_router(reports_router, tags=["reports"])
api_router.include_router(dashboard_router, tags=["dashboard"])
