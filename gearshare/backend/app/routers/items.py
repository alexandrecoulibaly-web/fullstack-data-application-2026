from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Response, status

from app.api.deps import DbSession
from app.repositories.item import ItemRepository
from app.schemas.item import ItemCreate, ItemRead, ItemUpdate
from app.services.item import ItemService

router = APIRouter(prefix="/items", tags=["items"])


def get_item_service(db: DbSession) -> ItemService:
    return ItemService(ItemRepository(db))


ItemServiceDependency = Annotated[ItemService, Depends(get_item_service)]


@router.get("", response_model=list[ItemRead])
def list_items(
    service: ItemServiceDependency,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    q: str | None = Query(default=None),
    disponible: bool | None = Query(default=None),
) -> list[ItemRead]:
    return service.list(skip=skip, limit=limit, query=q, disponible=disponible)


@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate, service: ItemServiceDependency) -> ItemRead:
    return service.create(payload)


@router.get("/{item_id}", response_model=ItemRead)
def get_item(
    service: ItemServiceDependency, item_id: int = Path(ge=1)
) -> ItemRead:
    return service.get(item_id)


@router.put("/{item_id}", response_model=ItemRead)
def replace_item(
    payload: ItemCreate,
    service: ItemServiceDependency,
    item_id: int = Path(ge=1),
) -> ItemRead:
    return service.replace(item_id, payload)


@router.patch("/{item_id}", response_model=ItemRead)
def update_item(
    payload: ItemUpdate,
    service: ItemServiceDependency,
    item_id: int = Path(ge=1),
) -> ItemRead:
    return service.update(item_id, payload)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    service: ItemServiceDependency, item_id: int = Path(ge=1)
) -> Response:
    service.delete(item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
