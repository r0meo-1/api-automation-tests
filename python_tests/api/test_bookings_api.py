import pytest


@pytest.mark.api
@pytest.mark.smoke
def test_get_booking_contract(api):
    session, base_url = api
    response = session.get(f"{base_url}/api/bookings/1", timeout=2)
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("application/json")
    assert response.json() == {"id": 1, "name": "Demo Guest", "nights": 2, "status": "confirmed"}


@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.parametrize("nights", [1, 28])
def test_create_booking_boundary_values(api, nights):
    session, base_url = api
    response = session.post(f"{base_url}/api/bookings", json={"name": "Roman", "nights": nights}, timeout=2)
    assert response.status_code == 201
    assert response.json()["nights"] == nights
    assert response.json()["status"] == "confirmed"


@pytest.mark.api
@pytest.mark.regression
@pytest.mark.parametrize(("payload", "error"), [
    ({"name": "", "nights": 2}, "name is required"),
    ({"nights": 2}, "name is required"),
    ({"name": "Roman", "nights": 0}, "nights must be 1..28"),
    ({"name": "Roman", "nights": 29}, "nights must be 1..28"),
    ({"name": "Roman", "nights": "2"}, "nights must be 1..28"),
])
def test_create_booking_rejects_invalid_payload(api, payload, error):
    session, base_url = api
    response = session.post(f"{base_url}/api/bookings", json=payload, timeout=2)
    assert response.status_code == 422
    assert response.json() == {"error": error}


@pytest.mark.api
@pytest.mark.regression
def test_create_booking_requires_json(api):
    session, base_url = api
    response = session.post(f"{base_url}/api/bookings", data="name=Roman&nights=2", headers={"Content-Type": "application/x-www-form-urlencoded"}, timeout=2)
    assert response.status_code == 415
    assert response.json() == {"error": "JSON required"}
