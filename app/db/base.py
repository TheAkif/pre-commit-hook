from sqlalchemy import Boolean
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column, as_declarative


@as_declarative()
class ORMBase:
    id: Mapped[int] = mapped_column(primary_key=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean(), nullable=True)

    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
