import os

os.environ.setdefault("DRY_RUN", "true")
os.environ.setdefault("OPENAI_API_KEY", "")

from fastapi.testclient import TestClient

from app.main import app
from app.offline import run_offline_crew
from app.tools import search_sops


client = TestClient(app)


def test_health_offline():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["mode"] == "offline"


def test_search_sops_cinta():
    hits = search_sops("cinta T901 emergencia LOTO", "data/sops")
    assert hits
    assert any("t901" in h["id"] for h in hits)


def test_offline_crew_sources():
    out = run_offline_crew("Atasco en cinta transportadora T901 con alarma")
    assert out["mode"] == "offline"
    assert out["sources"]
    assert "LOTO" in out["safety_review"]


def test_run_endpoint():
    r = client.post("/run", json={"task": "Cambio de molde en prensa T9013"})
    assert r.status_code == 200
    body = r.json()
    assert body["mode"] == "offline"
    assert body["plan"]
    assert body["technician_notes"]
