import traceback
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi_filter import FilterDepends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter(prefix="/items", tags=["items"])


def get_item(*, db: Session = Depends(deps.get_db), id: int) -> models.Item:
    item = crud.item.get(db=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found.")
    return item


@router.get("/", response_model=List[schemas.Item])
async def read_items(
    item_filter: models.ItemFilter = FilterDepends(models.ItemFilter),
    db: Session = Depends(deps.get_db),
) -> List[schemas.Item]:
    try:
        query = select(models.Item)
        query = item_filter.filter(query)
        result = db.execute(query).scalars().all()
    except Exception as e:
        print(traceback.format_exc())
        result = []
    return result


@router.post("/", response_model=schemas.Item)
def create_item(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.ItemCreate,
):
    """Create new item."""
    return crud.item.create(db, obj_in=item_in)


@router.patch("/{id}", response_model=schemas.Item)
def update_item(
    *,
    db: Session = Depends(deps.get_db),
    item: models.Item = Depends(get_item),
    item_in: schemas.ItemUpdate,
):
    """Update an item."""
    item = crud.item.update(db=db, db_obj=item, obj_in=item_in)
    return item


@router.get("/{id}", response_model=schemas.Item)
def read_item(
    *,
    item: models.Item = Depends(get_item),
):
    """Get item by id."""
    return item


@router.delete("/{id}", response_model=schemas.Item)
def delete_item(
    *,
    db: Session = Depends(deps.get_db),
    item: models.Item = Depends(get_item),
):
    """Delete an item."""
    item = crud.item.remove(db=db, id=item.id)
    return item
