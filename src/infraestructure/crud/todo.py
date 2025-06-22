"""
This file contains the CRUD operations for the Todo.
"""

from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlmodel import Session, select

from domain.models.todo import Todo
from domain.schemas.todo import TodoCreate, TodoUpdate
from infraestructure.crud.base import CRUDBase


class CRUDTodo(CRUDBase[Todo, TodoCreate, TodoUpdate]):
    """
    CRUD operations for the Todo.
    """

    def create(self, db: Session, obj_in: TodoCreate, todo_list_id: UUID) -> Todo:
        """
        Create a new Todo.
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, list_id=todo_list_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_all_by_list_id(
        self,
        db: Session,
        todo_list_id: UUID,
        name: str = None,
        order_by_completed: bool = False,
    ) -> list[Todo]:
        """
        Get all Todos by Todo List ID, with optional name filter and ordering by is_completed.
        """
        statement = select(self.model).where(self.model.list_id == todo_list_id)
        if name:
            statement = statement.where(self.model.title.ilike(f"%{name}%"))
        if order_by_completed:
            statement = statement.order_by(self.model.is_completed)
        results = db.exec(statement).all()
        total = len(results)
        return {"total": total, "data": results}

    def get_by_list_and_id(
        self, db: Session, todo_list_id: UUID, todo_id: UUID
    ) -> Todo:
        """
        Get a Todo by Todo List ID and Todo ID.
        """
        statement = select(self.model).where(
            self.model.list_id == todo_list_id, self.model.id == todo_id
        )
        return db.exec(statement).one_or_none()


todo = CRUDTodo(Todo)
