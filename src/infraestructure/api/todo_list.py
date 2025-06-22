"""
This file contains API endpoints for the Todo resource.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from domain.models.todo_list import TodoList
from domain.schemas.todo_list import (
    TodoListAll,
    TodoListCreate,
    TodoListResponse,
    TodoListUpdate,
)
from infraestructure.crud.todo_list import todo_list as todo_list_crud
from infraestructure.db.database import get_db

router = APIRouter()


@router.post("/", response_model=TodoListResponse)
def create_todo(todo: TodoListCreate, db=Depends(get_db)) -> TodoListResponse:
    """
    Create a new Todo.
    """
    todo = todo_list_crud.create(db, todo)
    return todo


@router.get("/", response_model=TodoListAll)
def get_all_todos(
    name: str = Query(None, description="Filter by name"), db=Depends(get_db)
) -> TodoListAll:
    """
    Get all Todos.
    """
    todos = todo_list_crud.all(db, name=name)
    return todos


@router.get("/{todo_list_id}", response_model=TodoList)
def get_todo(todo_list_id: UUID, db=Depends(get_db)) -> TodoList:
    """
    Get a single Todo
    """
    todo = todo_list_crud.get(db, todo_list_id)

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todo


@router.put("/{todo_list_id}", response_model=TodoList)
def update_todo(
    todo_list_id: UUID, obj_in: TodoListUpdate, db=Depends(get_db)
) -> TodoList:
    """
    Update a Todo List.
    """
    db_obj = todo_list_crud.get(db, todo_list_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo = todo_list_crud.update(db, db_obj, obj_in)
    return todo


@router.delete("/{todo_list_id}")
def delete_todo(todo_list_id: UUID, db=Depends(get_db)) -> TodoList:
    """
    Delete a Todo List.
    """
    todo = todo_list_crud.get(db, todo_list_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_list_crud.delete(db, todo_list_id)
    return todo
