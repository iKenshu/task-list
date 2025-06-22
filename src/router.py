"""
This file contains the routers for the application.
"""

from fastapi import APIRouter

from infraestructure.api.todo import router as todo_router
from infraestructure.api.todo_list import router as todo_list_router

api_router = APIRouter()

api_router.include_router(
    todo_router,
    prefix="/lists",
    tags=["todos"],
)

api_router.include_router(
    todo_list_router,
    prefix="/lists",
    tags=["todo_lists"],
)
