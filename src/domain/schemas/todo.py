from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TodoBase(BaseModel):
    """
    Todo Base Schema
    """

    title: str
    description: Optional[str] = None
    is_completed: bool = False
    todo_list_id: Optional[UUID] = None


class TodoCreate(BaseModel):
    """
    Todo Create Schema
    """

    title: str
    description: Optional[str] = None
    is_completed: bool = False


class TodoUpdate(BaseModel):
    """
    Todo Update Schema
    """

    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None


class TodoResponse(TodoBase):
    """
    Todo Response Schema
    """

    id: UUID
    model_config = ConfigDict(from_attributes=True)


class TodoAll(BaseModel):
    """
    Todo All Schema
    """

    total: int
    data: List[TodoResponse]
