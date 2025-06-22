"""
This file contains model definitions for the Todo.
"""

from typing import Optional
from uuid import UUID

from sqlmodel import Field, Relationship

from domain.models.base import Base
from domain.models.todo_list import TodoList


class Todo(Base, table=True):
    """
    Todo Model

    title: str
    description: Optional[str] = None
    is_completed: bool = Field(default=False)
    """

    title: str
    description: Optional[str] = None
    is_completed: bool = Field(default=False)

    list_id: UUID = Field(foreign_key="todolist.id")
    list: Optional[TodoList] = Relationship(back_populates="todos")
