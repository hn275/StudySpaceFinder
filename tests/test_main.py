from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_api_index():
    res = client.get("/")
    assert res.status_code == 200


# /api/building/all
def test_building_names():
    res = client.get("/api/buildings/all")
    assert res.status_code == 200

    body = res.json()
    assert isinstance(body, list)


# /api/buildings/{bldg_id}
def test_building_bad_time():
    def run_test(hour, minute):
        res = client.get(f"/api/buildings/1?hour={hour}&minute={minute}&day=0")
        assert res.status_code == 400

    run_test(25, 0)
    run_test(0, 61)
    run_test(-1, 30)
    run_test(1, -1)
    run_test(24, 1)


def test_building_bad_building():
    res = client.get("/api/buildings/1000000?hour=20&minute=20&day=1")
    assert res.status_code == 404


def test_building_detail():
    res = client.get("/api/buildings/1?hour=23&minute=30&day=1")
    assert res.status_code == 200

    payload = res.json()
    assert isinstance(payload["building"], str)
    assert isinstance(payload["data"], list)
