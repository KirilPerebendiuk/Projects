from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_returns_message():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "DevOps Task Platform API"}


def test_health_returns_healthy():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_tasks_returns_tasks():
    mock_cursor = MagicMock()
    mock_connection = MagicMock()

    mock_connection.__enter__.return_value = mock_connection
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.fetchall.return_value = [
        (1, "Learn Docker", "Practice containers", "pending", None),
        (2, "Learn Kubernetes", "Practice deployments", "pending", None),
    ]

    with patch("app.main.get_connection", return_value=mock_connection):
        response = client.get("/tasks")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["id"] == 1
    assert data[0]["title"] == "Learn Docker"
    assert data[1]["id"] == 2
    assert data[1]["title"] == "Learn Kubernetes"


def test_create_task_returns_created_task():
    mock_cursor = MagicMock()
    mock_connection = MagicMock()

    mock_connection.__enter__.return_value = mock_connection
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.fetchone.return_value = (
        10,
        "Learn Docker",
        "Practice containers",
        "pending",
        None,
    )

    with patch("app.main.get_connection", return_value=mock_connection):
        response = client.post(
            "/tasks",
            json={
                "title": "Learn Docker",
                "description": "Practice containers",
            },
        )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 10
    assert data["title"] == "Learn Docker"
    assert data["description"] == "Practice containers"
    assert data["status"] == "pending"

    mock_cursor.execute.assert_called_once()


def test_create_task_rejects_empty_title():
    with patch("app.main.get_connection") as mock_get_connection:
        response = client.post(
            "/tasks",
            json={
                "title": "",
                "description": "Practice containers",
            },
        )

    assert response.status_code == 422
    mock_get_connection.assert_not_called()
