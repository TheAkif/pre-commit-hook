from sqlalchemy.orm import Session

from app import crud, models, schemas
from tests.utils import random_lower_string


def create_random_item(db: Session, owner_id: int | None = None) -> models.Item:
    title = random_lower_string()
    description = random_lower_string()
    item_in = schemas.ItemCreate(title=title, description=description, owner_id=1)
    return crud.item.create(db, obj_in=item_in)
