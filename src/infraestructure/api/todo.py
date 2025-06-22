"""
This file contains API endpoints for the Todo resource.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from domain.models.todo import Todo
from domain.schemas.todo import TodoAll, TodoCreate, TodoResponse, TodoUpdate
from infraestructure.crud.todo import todo as todo_crud
from infraestructure.crud.todo_list import todo_list as todo_list_crud
from infraestructure.db.database import get_db

router = APIRouter()


@router.post("/{todo_list_id}/task", response_model=TodoResponse)
def create_todo(
    todo_list_id: UUID, todo: TodoCreate, db=Depends(get_db)
) -> TodoResponse:
    """
    Create a new Todo in a specific Todo List.
    """
    todo = todo_crud.create(db, todo, todo_list_id)
    return todo


@router.get("/{todo_list_id}/task", response_model=TodoAll)
def get_all_todos(todo_list_id: UUID, db=Depends(get_db)) -> TodoAll:
    """
    Get all Todos for a specific Todo List.
    """
    todos = todo_crud.get_all_by_list_id(db, todo_list_id)
    return todos


@router.get("/{todo_list_id}/task/{todo_id}", response_model=Todo)
def get_todo(todo_list_id: UUID, todo_id: UUID, db=Depends(get_db)) -> Todo:
    """
    Get a single Todo from a specific Todo List.
    """
    todo_list = todo_list_crud.get(db, todo_list_id)
    if not todo_list:
        raise HTTPException(status_code=404, detail="Todo list not found")

    todo = todo_crud.get_by_list_and_id(db, todo_list.id, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/{todo_list_id}/task/{todo_id}", response_model=Todo)
def update_todo(
    todo_list_id: UUID, todo_id: UUID, obj_in: TodoUpdate, db=Depends(get_db)
) -> Todo:
    """
    Update a Todo in a specific Todo List.
    """
    todo_list = todo_list_crud.get(db, todo_list_id)
    if not todo_list:
        raise HTTPException(status_code=404, detail="Todo list not found")

    db_obj = todo_crud.get_by_list_and_id(db, todo_list.id, todo_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo = todo_crud.update(db, db_obj, obj_in)
    return todo


@router.delete("/{todo_list_id}/task/{todo_id}")
def delete_todo(todo_list_id: UUID, todo_id: UUID, db=Depends(get_db)) -> Todo:
    """
    Delete a Todo from a specific Todo List.
    """
    todo_list = todo_list_crud.get(db, todo_list_id)
    if not todo_list:
        raise HTTPException(status_code=404, detail="Todo list not found")

    todo = todo_crud.get_by_list_and_id(db, todo_list.id, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo = todo_crud.delete(db, todo_id)
    return todo
