from fastapi.testclient import TestClient
from app.main import app
from app.logic import check_temperature, should_create_alert

client = TestClient(app)


# --- Logik tests ---

def test_normal_temperature():
    assert check_temperature(75.0) == "normal"

def test_warning_temperature():
    assert check_temperature(85.0) == "warning"

def test_critical_temperature():
    assert check_temperature(96.0) == "critical"

def test_exact_threshold_is_warning():
    assert check_temperature(80.0) == "warning"

def test_normal_no_alert():
    assert should_create_alert("normal") == False

def test_warning_creates_alert():
    assert should_create_alert("warning") == True

def test_critical_creates_alert():
    assert should_create_alert("critical") == True


# --- API tests ---

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"

def test_post_normal_reading():
    response = client.post("/turbine-readings", json={
        "turbine_id": "turbine-01",
        "temperature": 72.0,
        "unit": "celsius"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "normal"
    assert data["alert_created"] == False

def test_post_warning_reading():
    response = client.post("/turbine-readings", json={
        "turbine_id": "turbine-01",
        "temperature": 85.0,
        "unit": "celsius"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "warning"
    assert data["alert_created"] == True

def test_post_critical_reading():
    response = client.post("/turbine-readings", json={
        "turbine_id": "turbine-02",
        "temperature": 97.0,
        "unit": "celsius"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "critical"
    assert data["alert_created"] == True
