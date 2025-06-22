"""
This file contains the tests for the TodoList endpoints.
"""

from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from domain.schemas.todo_list import TodoListCreate
from infraestructure.crud.todo_list import todo_list as todo_list_crud
from infraestructure.db.database import get_db
from main import app

client = TestClient(app)


@pytest.fixture
def todo_list_id():
    db = get_db()
    todo_list = todo_list_crud.create(db, TodoListCreate(name="Test List"))
    return todo_list.id


def test_create_todo_list():
    response = client.post(
        "/api/lists/",
        json={"name": "Test List"},
    )
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "Test List"
    assert "id" in data


def test_get_all_todo_lists(todo_list_id):
    response = client.get("/api/lists/")
    data = response.json()
    assert response.status_code == 200
    assert data["total"] >= 1


def test_get_todo_list(todo_list_id):
    response = client.get(f"/api/lists/{todo_list_id}")
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == str(todo_list_id)
    assert data["name"] == "Test List"


def test_get_todo_list_not_found():
    response = client.get(f"/api/lists/{uuid4()}")
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Todo not found"


def test_update_todo_list(todo_list_id):
    response = client.put(
        f"/api/lists/{todo_list_id}",
        json={"name": "Updated List"},
    )
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "Updated List"


def test_update_todo_list_not_found():
    response = client.put(
        f"/api/lists/{uuid4()}",
        json={"name": "Updated List"},
    )
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Todo not found"


def test_delete_todo_list(todo_list_id):
    response = client.delete(f"/api/lists/{todo_list_id}")
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == str(todo_list_id)
    assert data["name"] == "Test List"


def test_delete_todo_list_not_found():
    response = client.delete(f"/api/lists/{uuid4()}")
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Todo not found"
    assert response.status_code == 404
    assert data["detail"] == "Todo not found"
