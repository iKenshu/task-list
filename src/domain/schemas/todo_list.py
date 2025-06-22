"""
This file contains the schemas for the Todo.
"""

from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TodoList(BaseModel):
    """
    Todo List Base Schema
    """

    name: str


class TodoListCreate(TodoList):
    """
    Todo List Create Schema
    """

    name: str


class TodoListUpdate(TodoList):
    """
    Todo List Update Schema
    """

    name: Optional[str]


class TodoListResponse(TodoList):
    """
    Todo List Response Schema
    """

    model_config = ConfigDict(from_attributes=True)
    id: UUID


class TodoListAll(BaseModel):
    """
    Todo List All Schema
    """

    total: int
    data: List[TodoListResponse]
