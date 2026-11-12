from app.core.exceptions import ResourceNotFound
from app.models.item import Item
from app.repositories.item import ItemRepository
from app.schemas.item import ItemCreate, ItemUpdate


class ItemService:
    def __init__(self, repository: ItemRepository) -> None:
        self.repository = repository

    def get(self, item_id: int) -> Item:
        item = self.repository.get(item_id)
        if item is None:
            raise ResourceNotFound(f"Item {item_id} introuvable")
        return item

    def list(
        self,
        *,
        skip: int = 0,
        limit: int = 20,
        query: str | None = None,
        disponible: bool | None = None,
    ) -> list[Item]:
        return self.repository.list(
            skip=skip, limit=limit, query=query, disponible=disponible
        )

    def create(self, payload: ItemCreate) -> Item:
        return self.repository.add(Item(**payload.model_dump()))

    def replace(self, item_id: int, payload: ItemCreate) -> Item:
        item = self.get(item_id)
        for field, value in payload.model_dump().items():
            setattr(item, field, value)
        return item

    def update(self, item_id: int, payload: ItemUpdate) -> Item:
        item = self.get(item_id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(item, field, value)
        return item

    def delete(self, item_id: int) -> None:
        item = self.get(item_id)
        self.repository.delete(item)
