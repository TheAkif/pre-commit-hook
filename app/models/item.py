from typing import Optional

from fastapi_filter.contrib.sqlalchemy import Filter
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import ORMBase


class Item(ORMBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    owner = relationship("User", back_populates="items")


class ItemFilter(Filter):
    title: Optional[str]
    description: Optional[str]
    description__like: Optional[str]

    class Constants(Filter.Constants):
        model = Item
        search_model_fields = ["title", "description"]
