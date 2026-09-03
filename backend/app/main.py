from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router

app = FastAPI(title="ReconPilot API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "ReconPilot backend is running"}


@app.get("/api/v1/health")
async def health():
    return {"status": "online", "project": "ReconPilot"}


@app.get("/api/status")
async def legacy_status():
    return {"status": "online", "project": "ReconPilot"}