from copy import deepcopy
import urllib.parse
from fastapi.testclient import TestClient
from src.app import app, activities

ORIGINAL = deepcopy(activities)
client = TestClient(app)


def setup_function(fn):
    # reset in-memory activities between tests
    activities.clear()
    activities.update(deepcopy(ORIGINAL))


def test_get_activities():
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_duplicate_and_delete():
    activity = "Chess Club"
    email = "tester@example.com"
    path = f"/activities/{urllib.parse.quote(activity)}/signup"

    # signup succeeds
    r1 = client.post(path, params={"email": email})
    assert r1.status_code == 200
    assert any(email == e for e in activities[activity]["participants"]) 

    # duplicate signup returns 400
    r2 = client.post(path, params={"email": email})
    assert r2.status_code == 400

    # delete (unregister) succeeds
    r3 = client.delete(path, params={"email": email})
    assert r3.status_code == 200
    assert all(e.lower() != email.lower() for e in activities[activity]["participants"]) 
