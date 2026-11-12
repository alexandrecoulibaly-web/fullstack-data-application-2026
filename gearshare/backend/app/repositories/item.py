from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.item import Item


class ItemRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, item_id: int) -> Item | None:
        statement = (
            select(Item)
            .options(joinedload(Item.owner))
            .where(Item.id == item_id)
        )
        return self.db.scalar(statement)

    def list(
        self,
        *,
        skip: int = 0,
        limit: int = 20,
        query: str | None = None,
        disponible: bool | None = None,
    ) -> list[Item]:
        statement = select(Item).options(joinedload(Item.owner))
        if query:
            statement = statement.where(Item.titre.ilike(f"%{query}%"))
        if disponible is not None:
            statement = statement.where(Item.disponible == disponible)
        statement = statement.offset(skip).limit(limit).order_by(Item.id)
        return list(self.db.scalars(statement))

    def add(self, item: Item) -> Item:
        self.db.add(item)
        self.db.flush()
        return item

    def delete(self, item: Item) -> None:
        self.db.delete(item)
        self.db.flush()
