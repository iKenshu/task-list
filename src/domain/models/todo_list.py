"""
This file contains model definitions for the Todo List.
"""

from sqlmodel import Relationship

from domain.models.base import Base


class TodoList(Base, table=True):
    """
    Todo Model

    Attributes:
        id: UUID
        is_active: bool
        date_created: datetime
        title: str
        description: Optional[str]
        is_completed: bool
    """

    name: str
    todos: list["Todo"] = Relationship(back_populates="list")
