# app/routers/items.py
from fastapi import APIRouter, HTTPException, Path, Query

from app.schemas.item import ItemCreate, ItemRead, ItemUpdate, ItemFilter

router = APIRouter(prefix="/items", tags=["items"])

FAKE_DB: dict[int, dict] = {}
_next_id = 1

@router.get(
    "/{item_id}",
    response_model=ItemRead,
    responses={404: {"description": "Item introuvable"}},
)
def get_item(item_id: int = Path(ge=1)):
    item = FAKE_DB.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} introuvable")
    return item

@router.get("", response_model=list[ItemFilter])
def list_items(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    q: str | None = None,
    disponible: bool | None = None,
):
    items = list(FAKE_DB.values())
    if q:
        items = [i for i in items if q.lower() in i["titre"]]
    if disponible is not None:
        items = [i for i in items if i["disponible"]]
    return items[skip : skip + limit]

@router.post("", response_model=ItemRead, status_code=201)
def create_item(payload: ItemCreate):
    global _next_id
    item = {"id": _next_id, **payload.model_dump()}
    FAKE_DB[_next_id] = item
    _next_id += 1
    return item

@router.put(
    "/{item_id}",
    response_model=ItemRead,
    status_code=200,
    responses={404: {"description": "Item introuvable"}},
)
def update_item(item_id: int, payload: ItemCreate):
    item = FAKE_DB.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} introuvable")
    item.update(payload.model_dump())
    return item

@router.patch(
    "/{item_id}",
    response_model=ItemRead,
    status_code=200,
    responses={404: {"description": "Item introuvable"}},
)
def patch_item(item_id: int, payload: ItemUpdate):
    item = FAKE_DB.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"Item {item_id} introuvable")
    item.update(payload.model_dump(exclude_unset=True))
    return item

@router.delete(
    "/{item_id}",
    status_code=204,
    responses={404: {"description": "Item introuvable"}},
)
def delete_item(item_id: int):
    if item_id not in FAKE_DB:
        raise HTTPException(status_code=404, detail=f"Item {item_id} introuvable")
    del FAKE_DB[item_id]