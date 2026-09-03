from fastapi.testclient import TestClient

from app.api.database.connection import ProjectRecord, SessionLocal
from app.main import app


client = TestClient(app)


def test_project_target_is_persisted_and_can_be_deleted():
	create_response = client.post(
		"/api/v1/projects",
		json={"name": "Internal gateway", "rootDomain": "https://192.0.2.50/"},
	)
	assert create_response.status_code == 200, create_response.text

	project = create_response.json()
	assert project["rootDomain"] == "192.0.2.50"

	with SessionLocal() as db:
		stored = db.get(ProjectRecord, project["id"])
		assert stored is not None
		assert stored.root_domain == "192.0.2.50"
		assert stored.name == "Internal gateway"

	delete_response = client.delete(f"/api/v1/projects/{project['id']}")
	assert delete_response.status_code == 200, delete_response.text
	assert client.get(f"/api/v1/projects/{project['id']}").status_code == 404

	with SessionLocal() as db:
		assert db.get(ProjectRecord, project["id"]) is None

	assert client.delete(f"/api/v1/projects/{project['id']}").status_code == 404


def test_project_rejects_invalid_target():
	response = client.post(
		"/api/v1/projects",
		json={"name": "Invalid target", "rootDomain": "not a target"},
	)

	assert response.status_code == 422
