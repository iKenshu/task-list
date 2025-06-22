"""
This file contains the CRUD operations for the Todo List.
"""

from domain.models.todo_list import TodoList
from domain.schemas.todo_list import TodoListCreate, TodoListUpdate
from infraestructure.crud.base import CRUDBase


class CRUDTodoList(CRUDBase[TodoList, TodoListCreate, TodoListUpdate]):
    """
    CRUD operations for the Todo List.
    """

    ...


todo_list = CRUDTodoList(TodoList)
todo_list = CRUDTodoList(TodoList)
