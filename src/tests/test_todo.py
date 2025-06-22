"""
This file contains the tests for the Todo.
"""

from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from domain.schemas.todo_list import TodoListCreate
from infraestructure.crud.todo import todo as todo_crud
from infraestructure.crud.todo_list import todo_list as todo_list_crud
from infraestructure.db.database import get_db
from main import app

client = TestClient(app)


@pytest.fixture
def todo_list_id():
    db = get_db()
    todo_list = todo_list_crud.create(db, TodoListCreate(name="Test List"))
    return todo_list.id


def test_create_todo(todo_list_id):
    """
    GIVEN a TodoCreate object
    WHEN a POST request is made to the /api/lists/{todo_list_id}/task endpoint
    THEN a 200 status code and the Todo object is returned
    """
    response = client.post(
        f"/api/lists/{str(todo_list_id)}/task",
        json={
            "title": "Test todo",
            "description": "Test description",
            "is_completed": False,
        },
    )

    data = response.json()
    assert response.status_code == 200
    assert data["title"] == "Test todo"
    assert data["description"] == "Test description"
    assert data["is_completed"] is False


def test_get_todos(todo_list_id):
    """
    GIVEN a TodoCreate object
    WHEN a GET request is made to the /api/lists/{todo_list_id}/task endpoint
    THEN a 200 status code and a list of Todo objects is returned
    """
    db = get_db()
    todo_crud.create(
        db,
        {
            "title": "Test todo",
            "description": "Test description",
            "is_completed": False,
        },
        todo_list_id,
    )
    response = client.get(f"/api/lists/{todo_list_id}/task")
    data = response.json()
    assert response.status_code == 200
    assert data["total"] >= 1
    assert any(todo["title"] == "Test todo" for todo in data["data"])


def test_get_todo(todo_list_id):
    """
    GIVEN a TodoCreate object
    WHEN a GET request is made to the /api/lists/{todo_list_id}/task endpoint
    THEN a 200 status code and the Todo object is returned
    """
    db = get_db()
    todo = todo_crud.create(
        db,
        {
            "title": "Test todo",
            "description": "Test description",
            "is_completed": False,
        },
        todo_list_id,
    )
    todo_id = todo.id
    response = client.get(f"/api/lists/{str(todo_list_id)}/task/{str(todo_id)}")
    data = response.json()
    assert response.status_code == 200
    assert data["title"] == "Test todo"
    assert data["description"] == "Test description"
    assert data["is_completed"] is False


def test_get_todo_not_found(todo_list_id):
    """
    GIVEN a TodoCreate object
    WHEN a GET request is made to the /api/lists/{todo_list_id}/tasks endpoint
    THEN a 404 status code and error message is returned
    """
    response = client.get(f"/api/lists/{todo_list_id}/task/{uuid4()}")
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Todo not found"


def test_get_todo__todo_list_not_found():
    """
    GIVEN a TodoCreate object
    WHEN a GET request is made to the /api/lists/{todo_list_id}/tasks endpoint
    THEN a 404 status code and error message is returned
    """
    response = client.get(f"/api/lists/{uuid4()}/task/{uuid4()}")
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Todo list not found"


def test_update_todo(todo_list_id):
    """
    GIVEN a TodoCreate object
    WHEN a PUT request is made to the /api/lists/{todo_list_id}/tasks endpoint
    THEN a 200 status code and the Todo object is returned
    """
    db = get_db()
    todo = todo_crud.create(
        db,
        {
            "title": "Test todo",
            "description": "Test description",
            "is_completed": False,
        },
        todo_list_id,
    )
    response = client.put(
        f"/api/lists/{str(todo_list_id)}/task/{str(todo.id)}",
        json={
            "title": "Test todo updated",
            "description": "Test description updated",
            "is_completed": True,
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data["title"] == "Test todo updated"
    assert data["description"] == "Test description updated"
    assert data["is_completed"] is True


def test_update_todo_not_found(todo_list_id):
    """
    GIVEN a TodoCreate object
    WHEN a PUT request is made to the /api/lists/{todo_list_id}/tasks endpoint
    THEN a 404 status code and error message is returned
    """
    response = client.put(
        f"/api/lists/{todo_list_id}/task/{uuid4()}",
        json={
            "title": "Test todo updated",
            "description": "Test description updated",
            "is_completed": True,
        },
    )
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Todo not found"


def test_update_todo__todo_list_not_found():
    """
    GIVEN a TodoCreate object
    WHEN a PUT request is made to the /api/lists/{todo_list_id}/tasks endpoint
    THEN a 404 status code and error message is returned
    """
    response = client.put(
        f"/api/lists/{uuid4()}/task/{uuid4()}",
        json={
            "title": "Test todo updated",
            "description": "Test description updated",
            "is_completed": True,
        },
    )
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Todo list not found"


def test_delete_todo(todo_list_id):
    """
    GIVEN a TodoCreate object
    WHEN a DELETE request is made to the /api/lists/{todo_list_id}/tasks endpoint
    THEN a 200 status code and the Todo object is returned
    """
    todo = todo_crud.create(
        get_db(),
        {
            "title": "Test todo",
            "description": "Test description",
            "is_completed": False,
        },
        todo_list_id,
    )

    response = client.delete(f"/api/lists/{str(todo_list_id)}/task/{str(todo.id)}")
    data = response.json()
    assert response.status_code == 200
    assert data["title"] == "Test todo"
    assert data["description"] == "Test description"
    assert data["is_completed"] is False


def test_delete_todo_not_found(todo_list_id):
    """
    GIVEN a TodoCreate object
    WHEN a DELETE request is made to the /api/lists/{todo_list_id}/tasks endpoint
    THEN a 404 status code and error message is returned
    """
    response = client.delete(f"/api/lists/{todo_list_id}/task/{uuid4()}")
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Todo not found"


def test_delete_todo__todo_list_not_found():
    """
    GIVEN a TodoCreate object
    WHEN a DELETE request is made to the /api/lists/{todo_list_id}/tasks endpoint
    THEN a 404 status code and error message is returned
    """
    response = client.delete(f"/api/lists/{uuid4()}/task/{uuid4()}")
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Todo list not found"
