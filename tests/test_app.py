import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    initial_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Practice and compete in basketball games",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Soccer Club": {
            "description": "Train and play soccer matches",
            "schedule": "Wednesdays and Saturdays, 3:00 PM - 5:00 PM",
            "max_participants": 22,
            "participants": ["liam@mergington.edu", "ava@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore painting, drawing, and creative arts",
            "schedule": "Mondays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu"]
        },
        "Drama Club": {
            "description": "Act in plays and learn theater skills",
            "schedule": "Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 20,
            "participants": ["mason@mergington.edu", "charlotte@mergington.edu"]
        },
        "Debate Club": {
            "description": "Develop argumentation and public speaking skills",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["ethan@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore scientific concepts",
            "schedule": "Tuesdays, 3:00 PM - 4:30 PM",
            "max_participants": 25,
            "participants": ["harper@mergington.edu", "logan@mergington.edu"]
        }
    }

    activities.clear()
    activities.update(initial_activities)
    yield
    activities.clear()
    activities.update(initial_activities)


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_keys = {
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Soccer Club",
        "Art Club",
        "Drama Club",
        "Debate Club",
        "Science Club"
    }

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, dict)
    assert set(result.keys()) == expected_keys


def test_signup_for_activity_adds_participant(client):
    # Arrange
    email = "newstudent@mergington.edu"
    activity_name = "Chess Club"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"


def test_signup_duplicate_returns_400(client):
    # Arrange
    email = "michael@mergington.edu"
    activity_name = "Chess Club"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_nonexistent_activity_returns_404(client):
    # Arrange
    email = "student@mergington.edu"
    activity_name = "Nonexistent Club"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_removes_participant(client):
    # Arrange
    email = "michael@mergington.edu"
    activity_name = "Chess Club"
    assert email in activities[activity_name]["participants"]

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Removed {email} from {activity_name}"


def test_remove_nonexistent_participant_returns_404(client):
    # Arrange
    email = "nonexistent@mergington.edu"
    activity_name = "Chess Club"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"


def test_root_redirects_to_static_html(client):
    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in {307, 308}
    assert response.headers["location"] == "/static/index.html"
