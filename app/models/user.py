from datetime import datetime
from typing import List, Optional

from fastapi_filter.contrib.sqlalchemy import Filter
from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, deferred, mapped_column, relationship

from app.db.base import ORMBase


class User(ORMBase):
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    hashed_password: Mapped[str] = deferred(
        mapped_column(String, unique=True, index=True)
    )
    full_name: Mapped[str] = mapped_column(String(32), default="none")
    date_of_joining: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    contact_number: Mapped[str] = mapped_column(String(32), nullable=True)
    address: Mapped[str] = mapped_column(String(200), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    items = relationship("Item", back_populates="owner")


class UserFilter(Filter):
    full_name: Optional[str]
    address: Optional[str]
    full_name__like: Optional[str]
    full_name_like: Optional[List[str]]

    class Constants(Filter.Constants):
        model = User
        search_model_fields = ["full_name", "address"]
