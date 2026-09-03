from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from sqlalchemy import delete, select

from app.api.database.connection import ProjectRecord, Record, SessionLocal, initialize_database
from app.api.workers.recon_worker import build_records, discover


class ReconPilotService:
    def __init__(self) -> None:
        initialize_database()
        self.projects = []
        self.scans = []
        self.assets = []
        self.endpoints = []
        self.javascript_files = []
        self.api_specs = []
        self.technologies = []
        self.queue_items = []
        self._load_or_seed_database()

    def _load_or_seed_database(self) -> None:
        with SessionLocal() as db:
            self._remove_legacy_seed_data(db)
            if db.query(Record).count() == 0:
                for kind, records in self._records_by_kind().items():
                    db.add_all(
                        Record(
                            id=record["id"],
                            kind=kind,
                            project_id=record.get("projectId"),
                            payload=record,
                        )
                        for record in records
                    )
                db.commit()
            else:
                stored = db.scalars(select(Record)).all()
                for kind, attribute in self._kind_attributes().items():
                    setattr(
                        self,
                        attribute,
                        [record.payload for record in stored if record.kind == kind],
                    )

            stored_projects = {project.id for project in db.scalars(select(ProjectRecord)).all()}
            for project in self.projects:
                if project["id"] not in stored_projects:
                    self._save_project_record(db, project)
            db.commit()

    @staticmethod
    def _remove_legacy_seed_data(db: Any) -> None:
        legacy_ids = {
            "p-001",
            "p-002",
            "p-003",
        }
        legacy_ids.update({
            project.id
            for project in db.scalars(select(ProjectRecord)).all()
            if project.root_domain in {"acme.test", "lab.local", "demo.example.com"}
        })
        for record in db.scalars(select(Record)).all():
            payload = record.payload
            if (
                record.id in legacy_ids
                or record.project_id in legacy_ids
                or payload.get("projectId") in legacy_ids
                or payload.get("endpoint", {}).get("projectId") in legacy_ids
            ):
                db.delete(record)
        for project_id in legacy_ids:
            project = db.get(ProjectRecord, project_id)
            if project is not None:
                db.delete(project)

    @staticmethod
    def _save_project_record(db: Any, project: dict[str, Any]) -> None:
        record = db.get(ProjectRecord, project["id"])
        values = {
            "name": project["name"],
            "root_domain": project["rootDomain"],
            "description": project.get("description"),
            "status": project.get("status", "active"),
            "asset_count": project.get("assetCount", 0),
            "endpoint_count": project.get("endpointCount", 0),
            "last_scan_at": project.get("lastScanAt"),
            "created_at": project["createdAt"],
        }
        if record is None:
            db.add(ProjectRecord(id=project["id"], **values))
        else:
            for key, value in values.items():
                setattr(record, key, value)

    def _records_by_kind(self) -> dict[str, list[dict[str, Any]]]:
        return {
            "project": self.projects,
            "scan": self.scans,
            "asset": self.assets,
            "endpoint": self.endpoints,
            "javascript": self.javascript_files,
            "api": self.api_specs,
            "technology": self.technologies,
            "queue": self.queue_items,
        }

    @staticmethod
    def _kind_attributes() -> dict[str, str]:
        return {
            "project": "projects",
            "scan": "scans",
            "asset": "assets",
            "endpoint": "endpoints",
            "javascript": "javascript_files",
            "api": "api_specs",
            "technology": "technologies",
            "queue": "queue_items",
        }

    def _save_records(self, records: list[tuple[str, dict[str, Any]]]) -> None:
        with SessionLocal() as db:
            for kind, payload in records:
                existing = db.get(Record, payload["id"])
                if existing is None:
                    db.add(
                        Record(
                            id=payload["id"],
                            kind=kind,
                            project_id=payload.get("projectId"),
                            payload=payload,
                        )
                    )
                else:
                    existing.kind = kind
                    existing.project_id = payload.get("projectId")
                    existing.payload = payload
                if kind == "project":
                    self._save_project_record(db, payload)
            db.commit()

    @staticmethod
    def _utc_now() -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def _normalize_root_domain(value: str) -> str:
        from app.api.schemas.project import normalize_target

        cleaned = normalize_target(value)
        return cleaned[4:] if cleaned.startswith("www.") else cleaned

    def _seed_projects(self) -> list[dict[str, Any]]:
        now = self._utc_now()
        return [
            {
                "id": "p-001",
                "name": "Acme Bug Bounty",
                "rootDomain": "acme.test",
                "description": "Authorized bug-bounty research workspace",
                "status": "active",
                "assetCount": 42,
                "endpointCount": 318,
                "lastScanAt": "2026-08-28T06:40:00Z",
                "createdAt": "2026-08-20T08:00:00Z",
            },
            {
                "id": "p-002",
                "name": "Local Lab",
                "rootDomain": "lab.local",
                "description": "Local application security lab",
                "status": "active",
                "assetCount": 8,
                "endpointCount": 76,
                "lastScanAt": "2026-08-27T18:20:00Z",
                "createdAt": "2026-08-15T09:30:00Z",
            },
            {
                "id": "p-003",
                "name": "Client Demo",
                "rootDomain": "demo.example.com",
                "description": "Sample recon workspace for validation",
                "status": "active",
                "assetCount": 0,
                "endpointCount": 0,
                "lastScanAt": now,
                "createdAt": now,
            },
        ]

    def _seed_scans(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "scan-001",
                "projectId": "p-001",
                "target": "acme.test",
                "status": "completed",
                "startedAt": "2026-08-28T06:00:00Z",
                "completedAt": "2026-08-28T06:40:00Z",
                "assetsFound": 42,
                "liveHosts": 27,
                "urlsFound": 1240,
                "jsFiles": 63,
                "apiEndpoints": 318,
                "technologies": 14,
                "progress": 100,
            },
            {
                "id": "scan-002",
                "projectId": "p-001",
                "target": "acme.test",
                "status": "running",
                "startedAt": "2026-08-28T08:05:00Z",
                "assetsFound": 44,
                "liveHosts": 29,
                "urlsFound": 1452,
                "jsFiles": 71,
                "apiEndpoints": 347,
                "technologies": 15,
                "progress": 72,
            },
            {
                "id": "scan-003",
                "projectId": "p-002",
                "target": "lab.local",
                "status": "completed",
                "startedAt": "2026-08-27T17:30:00Z",
                "completedAt": "2026-08-27T18:20:00Z",
                "assetsFound": 8,
                "liveHosts": 8,
                "urlsFound": 410,
                "jsFiles": 19,
                "apiEndpoints": 76,
                "technologies": 9,
                "progress": 100,
            },
        ]

    def _seed_assets(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "asset-001",
                "projectId": "p-001",
                "hostname": "app.acme.test",
                "url": "https://app.acme.test",
                "type": "subdomain",
                "statusCode": 200,
                "alive": True,
                "title": "Acme Dashboard",
                "technologies": ["React", "Nginx", "Node.js"],
                "ips": ["192.0.2.10"],
                "ports": [443, 80],
                "source": ["subfinder", "httpx"],
                "discoveredAt": "2026-08-28T06:02:00Z",
            },
            {
                "id": "asset-002",
                "projectId": "p-001",
                "hostname": "api.acme.test",
                "url": "https://api.acme.test",
                "type": "subdomain",
                "statusCode": 200,
                "alive": True,
                "title": "Acme API",
                "technologies": ["FastAPI", "Nginx"],
                "ips": ["192.0.2.11"],
                "ports": [443],
                "source": ["subfinder", "httpx", "katana"],
                "discoveredAt": "2026-08-28T06:03:00Z",
            },
            {
                "id": "asset-003",
                "projectId": "p-001",
                "hostname": "admin.acme.test",
                "url": "https://admin.acme.test",
                "type": "subdomain",
                "statusCode": 403,
                "alive": True,
                "title": "Forbidden",
                "technologies": ["Nginx"],
                "ips": ["192.0.2.12"],
                "ports": [443],
                "source": ["subfinder", "httpx"],
                "discoveredAt": "2026-08-28T06:04:00Z",
            },
            {
                "id": "asset-004",
                "projectId": "p-001",
                "hostname": "cdn.acme.test",
                "url": "https://cdn.acme.test",
                "type": "subdomain",
                "statusCode": 200,
                "alive": True,
                "title": "Acme CDN",
                "technologies": ["CloudFront"],
                "ips": ["192.0.2.13"],
                "ports": [443],
                "source": ["subfinder"],
                "discoveredAt": "2026-08-28T06:05:00Z",
            },
        ]

    def _seed_endpoints(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "ep-001",
                "projectId": "p-001",
                "host": "api.acme.test",
                "method": "GET",
                "path": "/api/users/{id}",
                "url": "https://api.acme.test/api/users/{id}",
                "category": "authorization",
                "priority": "high",
                "authRequired": True,
                "parameterCount": 1,
                "parameters": ["id"],
                "statusCode": 200,
                "contentType": "application/json",
                "sources": ["katana", "javascript", "openapi"],
                "notes": "Object identifier; review ownership enforcement.",
                "lastSeenAt": "2026-08-28T06:31:00Z",
            },
            {
                "id": "ep-002",
                "projectId": "p-001",
                "host": "api.acme.test",
                "method": "POST",
                "path": "/api/auth/login",
                "url": "https://api.acme.test/api/auth/login",
                "category": "authentication",
                "priority": "high",
                "authRequired": False,
                "parameterCount": 2,
                "parameters": ["email", "password"],
                "statusCode": 200,
                "contentType": "application/json",
                "sources": ["katana", "javascript"],
                "lastSeenAt": "2026-08-28T06:30:00Z",
            },
            {
                "id": "ep-003",
                "projectId": "p-001",
                "host": "api.acme.test",
                "method": "POST",
                "path": "/api/transfers",
                "url": "https://api.acme.test/api/transfers",
                "category": "business-logic",
                "priority": "critical",
                "authRequired": True,
                "parameterCount": 3,
                "parameters": ["from", "to", "amount"],
                "statusCode": 201,
                "contentType": "application/json",
                "sources": ["openapi", "javascript"],
                "notes": "Business operation; manually review state transitions and limits.",
                "lastSeenAt": "2026-08-28T06:33:00Z",
            },
            {
                "id": "ep-004",
                "projectId": "p-001",
                "host": "app.acme.test",
                "method": "POST",
                "path": "/api/upload",
                "url": "https://app.acme.test/api/upload",
                "category": "file-upload",
                "priority": "high",
                "authRequired": True,
                "parameterCount": 1,
                "parameters": ["file"],
                "statusCode": 200,
                "contentType": "application/json",
                "sources": ["katana"],
                "lastSeenAt": "2026-08-28T06:25:00Z",
            },
            {
                "id": "ep-005",
                "projectId": "p-001",
                "host": "admin.acme.test",
                "method": "GET",
                "path": "/admin/users",
                "url": "https://admin.acme.test/admin/users",
                "category": "admin",
                "priority": "high",
                "authRequired": True,
                "parameterCount": 0,
                "parameters": [],
                "statusCode": 403,
                "contentType": "text/html",
                "sources": ["katana", "javascript"],
                "lastSeenAt": "2026-08-28T06:21:00Z",
            },
            {
                "id": "ep-006",
                "projectId": "p-001",
                "host": "api.acme.test",
                "method": "POST",
                "path": "/graphql",
                "url": "https://api.acme.test/graphql",
                "category": "graphql",
                "priority": "medium",
                "authRequired": True,
                "parameterCount": 1,
                "parameters": ["query"],
                "statusCode": 200,
                "contentType": "application/json",
                "sources": ["katana", "javascript"],
                "lastSeenAt": "2026-08-28T06:35:00Z",
            },
            {
                "id": "ep-007",
                "projectId": "p-001",
                "host": "api.acme.test",
                "method": "POST",
                "path": "/api/password/reset",
                "url": "https://api.acme.test/api/password/reset",
                "category": "authentication",
                "priority": "high",
                "authRequired": False,
                "parameterCount": 1,
                "parameters": ["email"],
                "statusCode": 202,
                "contentType": "application/json",
                "sources": ["javascript"],
                "lastSeenAt": "2026-08-28T06:36:00Z",
            },
        ]

    def _seed_javascript_files(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "js-001",
                "projectId": "p-001",
                "host": "app.acme.test",
                "url": "https://app.acme.test/assets/app.82a91.js",
                "filename": "app.82a91.js",
                "size": 842301,
                "endpointsFound": 31,
                "secretsFound": 0,
                "source": "katana",
                "statusCode": 200,
                "lastSeenAt": "2026-08-28T06:22:00Z",
            },
            {
                "id": "js-002",
                "projectId": "p-001",
                "host": "app.acme.test",
                "url": "https://app.acme.test/assets/auth.2ab81.js",
                "filename": "auth.2ab81.js",
                "size": 182210,
                "endpointsFound": 17,
                "secretsFound": 0,
                "source": "katana",
                "statusCode": 200,
                "lastSeenAt": "2026-08-28T06:23:00Z",
            },
            {
                "id": "js-003",
                "projectId": "p-001",
                "host": "admin.acme.test",
                "url": "https://admin.acme.test/static/admin.js",
                "filename": "admin.js",
                "size": 491223,
                "endpointsFound": 22,
                "secretsFound": 0,
                "source": "javascript",
                "statusCode": 403,
                "lastSeenAt": "2026-08-28T06:24:00Z",
            },
        ]

    def _seed_api_specs(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "api-001",
                "projectId": "p-001",
                "host": "api.acme.test",
                "type": "OpenAPI",
                "url": "https://api.acme.test/openapi.json",
                "version": "3.0.3",
                "endpointCount": 184,
                "discoveredAt": "2026-08-28T06:15:00Z",
                "statusCode": 200,
            },
            {
                "id": "api-002",
                "projectId": "p-001",
                "host": "api.acme.test",
                "type": "GraphQL",
                "url": "https://api.acme.test/graphql",
                "endpointCount": 1,
                "discoveredAt": "2026-08-28T06:16:00Z",
                "statusCode": 200,
            },
        ]

    def _seed_technologies(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "tech-001",
                "projectId": "p-001",
                "name": "React",
                "category": "frontend",
                "version": "19.x",
                "assets": 12,
                "confidence": 98,
                "sources": ["httpx", "javascript"],
            },
            {
                "id": "tech-002",
                "projectId": "p-001",
                "name": "Nginx",
                "category": "server",
                "version": "1.x",
                "assets": 24,
                "confidence": 96,
                "sources": ["httpx"],
            },
            {
                "id": "tech-003",
                "projectId": "p-001",
                "name": "Node.js",
                "category": "backend",
                "version": "22.x",
                "assets": 7,
                "confidence": 91,
                "sources": ["httpx", "javascript"],
            },
            {
                "id": "tech-004",
                "projectId": "p-001",
                "name": "FastAPI",
                "category": "backend",
                "version": "0.x",
                "assets": 3,
                "confidence": 87,
                "sources": ["httpx", "openapi"],
            },
        ]

    def _seed_queue_items(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "queue-001",
                "endpointId": "ep-003",
                "endpoint": self.endpoints[2],
                "reason": "Business operation with multiple user-controlled identifiers and an amount field.",
                "priority": "critical",
                "aiScore": 97,
                "status": "new",
                "createdAt": "2026-08-28T06:34:00Z",
            },
            {
                "id": "queue-002",
                "endpointId": "ep-001",
                "endpoint": self.endpoints[0],
                "reason": "Object-level endpoint containing a user-controlled object identifier.",
                "priority": "high",
                "aiScore": 94,
                "status": "new",
                "createdAt": "2026-08-28T06:32:00Z",
            },
            {
                "id": "queue-003",
                "endpointId": "ep-004",
                "endpoint": self.endpoints[3],
                "reason": "Authenticated file upload endpoint discovered during crawl.",
                "priority": "high",
                "aiScore": 89,
                "status": "testing",
                "createdAt": "2026-08-28T06:26:00Z",
            },
            {
                "id": "queue-004",
                "endpointId": "ep-007",
                "endpoint": self.endpoints[6],
                "reason": "Unauthenticated password-reset workflow.",
                "priority": "high",
                "aiScore": 88,
                "status": "new",
                "createdAt": "2026-08-28T06:37:00Z",
            },
        ]

    def list_projects(self) -> list[dict[str, Any]]:
        return [project.copy() for project in self.projects]

    def get_project(self, project_id: str) -> dict[str, Any] | None:
        for project in self.projects:
            if project["id"] == project_id:
                return project.copy()
        return None

    def create_project(self, payload: dict[str, Any]) -> dict[str, Any]:
        root_domain = self._normalize_root_domain(payload.get("rootDomain") or payload.get("target") or payload.get("name") or "example.com")
        project_name = payload.get("name") or root_domain
        project_numbers = [
            int(project["id"].split("-", 1)[1])
            for project in self.projects
            if project["id"].startswith("p-") and project["id"].split("-", 1)[1].isdigit()
        ]
        project_id = f"p-{max(project_numbers, default=0) + 1:03d}"
        now = self._utc_now()
        project = {
            "id": project_id,
            "name": project_name,
            "rootDomain": root_domain,
            "description": payload.get("description") or f"Recon workspace for {root_domain}",
            "status": "active",
            "assetCount": 0,
            "endpointCount": 0,
            "lastScanAt": now,
            "createdAt": now,
        }
        self.projects.append(project)
        initial_scan = {
                "id": f"scan-{len(self.scans) + 1:03d}",
                "projectId": project_id,
                "target": root_domain,
                "status": "queued",
                "startedAt": now,
                "assetsFound": 0,
                "liveHosts": 0,
                "urlsFound": 0,
                "jsFiles": 0,
                "apiEndpoints": 0,
                "technologies": 0,
                "progress": 5,
            }
        self.scans.append(initial_scan)
        initial_asset = {
                "id": f"asset-{len(self.assets) + 1:03d}",
                "projectId": project_id,
                "hostname": root_domain,
                "url": f"https://{root_domain}",
                "type": "domain",
                "statusCode": 200,
                "alive": True,
                "title": root_domain,
                "technologies": [],
                "ips": [],
                "ports": [443],
                "source": ["manual"],
                "discoveredAt": now,
            }
        self.assets.append(initial_asset)
        initial_endpoint = {
            "id": f"ep-{len(self.endpoints) + 1:03d}",
            "projectId": project_id,
            "host": root_domain,
            "method": "GET",
            "path": "/",
            "url": f"https://{root_domain}",
            "category": "general",
            "priority": "info",
            "authRequired": False,
            "parameterCount": 0,
            "parameters": [],
            "statusCode": 200,
            "sources": ["manual"],
            "lastSeenAt": now,
        }
        self.endpoints.append(initial_endpoint)
        project["assetCount"] = 1
        project["endpointCount"] = 1
        self._save_records(
            [("project", project), ("scan", initial_scan), ("asset", initial_asset), ("endpoint", initial_endpoint)]
        )
        return project.copy()

    def delete_project(self, project_id: str) -> bool:
        if self.get_project(project_id) is None:
            return False

        for collection_name in (
            "projects",
            "scans",
            "assets",
            "endpoints",
            "javascript_files",
            "api_specs",
            "technologies",
        ):
            collection = getattr(self, collection_name)
            setattr(
                self,
                collection_name,
                [
                    item
                    for item in collection
                    if item.get("id") != project_id and item.get("projectId") != project_id
                ],
            )
        self.queue_items = [
            item
            for item in self.queue_items
            if item.get("endpoint", {}).get("projectId") != project_id
        ]

        with SessionLocal() as db:
            records = db.scalars(select(Record)).all()
            for record in records:
                payload = record.payload
                if (
                    record.id == project_id
                    or payload.get("projectId") == project_id
                    or payload.get("endpoint", {}).get("projectId") == project_id
                ):
                    db.delete(record)
            db.execute(delete(ProjectRecord).where(ProjectRecord.id == project_id))
            db.commit()
        return True

    def list_scans(self, project_id: str | None = None) -> list[dict[str, Any]]:
        scans = self.scans
        if project_id:
            scans = [scan for scan in scans if scan["projectId"] == project_id]
        return [scan.copy() for scan in scans]

    def get_scan(self, scan_id: str) -> dict[str, Any] | None:
        for scan in self.scans:
            if scan["id"] == scan_id:
                return scan.copy()
        return None

    def start_scan(self, project_id: str, target: str | None = None) -> dict[str, Any]:
        project = self.get_project(project_id)
        if project is None:
            raise ValueError("Project not found")
        scan_target = self._normalize_root_domain(target or project["rootDomain"])

        scan_id = f"scan-{len(self.scans) + 1:03d}"
        payload = {
            "id": scan_id,
            "projectId": project_id,
            "target": scan_target,
            "status": "running",
            "startedAt": self._utc_now(),
            "assetsFound": 0,
            "liveHosts": 0,
            "urlsFound": 0,
            "jsFiles": 0,
            "apiEndpoints": 0,
            "technologies": 0,
            "progress": 10,
        }
        self.scans.insert(0, payload)
        self._save_records([("scan", payload)])
        try:
            result = discover(payload["target"])
            assets, endpoints, javascript, technologies = build_records(result, project_id)
            self.assets.extend(assets)
            self.endpoints.extend(endpoints)
            self.javascript_files.extend(javascript)
            self.technologies.extend(technologies)
            payload.update({
                "status": "completed",
                "assetsFound": len(assets),
                "liveHosts": sum(1 for item in assets if item["alive"]),
                "urlsFound": len(result.urls),
                "jsFiles": len(javascript),
                "apiEndpoints": len(endpoints),
                "technologies": len(technologies),
                "progress": 100,
            })
        except Exception:
            payload.update({"status": "failed", "progress": 100})
        project["lastScanAt"] = payload["startedAt"]
        project["assetCount"] = sum(1 for item in self.assets if item.get("projectId") == project_id)
        project["endpointCount"] = sum(1 for item in self.endpoints if item.get("projectId") == project_id)
        for stored_project in self.projects:
            if stored_project["id"] == project_id:
                stored_project.update(project)
                break
        self._save_records(
            [("scan", payload)]
            + [("asset", item) for item in self.assets if item.get("projectId") == project_id]
            + [("endpoint", item) for item in self.endpoints if item.get("projectId") == project_id]
            + [("javascript", item) for item in self.javascript_files if item.get("projectId") == project_id]
            + [("technology", item) for item in self.technologies if item.get("projectId") == project_id]
        )
        self._save_records([("project", project)])
        return payload.copy()

    def list_assets(self, project_id: str | None = None) -> list[dict[str, Any]]:
        items = self.assets
        if project_id:
            items = [item for item in items if item["projectId"] == project_id]
        return [item.copy() for item in items]

    def list_endpoints(self, project_id: str | None = None) -> list[dict[str, Any]]:
        items = self.endpoints
        if project_id:
            items = [item for item in items if item["projectId"] == project_id]
        return [item.copy() for item in items]

    def list_javascript_files(self, project_id: str | None = None) -> list[dict[str, Any]]:
        items = self.javascript_files
        if project_id:
            items = [item for item in items if item["projectId"] == project_id]
        return [item.copy() for item in items]

    def list_api_specs(self, project_id: str | None = None) -> list[dict[str, Any]]:
        items = self.api_specs
        if project_id:
            items = [item for item in items if item["projectId"] == project_id]
        return [item.copy() for item in items]

    def list_technologies(self, project_id: str | None = None) -> list[dict[str, Any]]:
        items = self.technologies
        if project_id:
            items = [item for item in items if item["projectId"] == project_id]
        return [item.copy() for item in items]

    def list_queue_items(self, project_id: str | None = None) -> list[dict[str, Any]]:
        items = self.queue_items
        if project_id:
            items = [item for item in items if item["endpoint"]["projectId"] == project_id]
        return [item.copy() for item in items]

    def get_dashboard_stats(self) -> dict[str, int]:
        return {
            "projects": len(self.projects),
            "assets": len(self.assets),
            "liveHosts": sum(1 for asset in self.assets if asset.get("alive")),
            "endpoints": len(self.endpoints),
            "jsFiles": len(self.javascript_files),
            "apiSpecs": len(self.api_specs),
            "technologies": len(self.technologies),
            "queueItems": len(self.queue_items),
        }


service = ReconPilotService()
