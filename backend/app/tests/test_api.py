from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_projects_and_dashboard_endpoints():
    project_payload = {
        "name": "Demo Project",
        "rootDomain": "demo.example.com",
        "description": "Authorized recon workspace",
    }

    create_response = client.post("/api/v1/projects", json=project_payload)
    assert create_response.status_code == 200, create_response.text

    project = create_response.json()
    assert project["name"] == project_payload["name"]
    assert project["rootDomain"] == project_payload["rootDomain"]

    list_response = client.get("/api/v1/projects")
    assert list_response.status_code == 200, list_response.text
    assert any(item["id"] == project["id"] for item in list_response.json())

    detail_response = client.get(f"/api/v1/projects/{project['id']}")
    assert detail_response.status_code == 200, detail_response.text
    assert detail_response.json()["id"] == project["id"]

    scans_response = client.get(f"/api/v1/projects/{project['id']}/scans")
    assert scans_response.status_code == 200, scans_response.text
    assert len(scans_response.json()) >= 1

    dashboard_response = client.get("/api/v1/dashboard")
    assert dashboard_response.status_code == 200, dashboard_response.text
    stats = dashboard_response.json()
    assert stats["projects"] >= 1
    assert stats["assets"] >= 1
    assert stats["endpoints"] >= 1
