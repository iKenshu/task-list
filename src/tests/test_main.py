"""
This file contains the tests for the main file.
"""

from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_lifespan():
    """
    GIVEN the application lifespan
    WHEN the application starts and stops
    THEN the init_db function should be called
    """
    with patch("main.init_db") as mock_init_db:
        with client:
            mock_init_db.assert_called_once()


def test_root():
    """
    GIVEN the root endpoint
    WHEN the application starts
    THEN the root endpoint should return a 200 status code
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Go to /docs"}
