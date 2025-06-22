"""
This is a base class for all models
"""

from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Base(SQLModel):
    """
    Base class for all models

    Attributes:
        id: UUID
        is_active: bool
        date_created: datetime
    """

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
    )
    is_active: bool = Field(default=True)
