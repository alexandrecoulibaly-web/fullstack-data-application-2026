from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.reservation import Reservation


class ReservationRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, reservation_id: int) -> Reservation | None:
        statement = (
            select(Reservation)
            .options(joinedload(Reservation.item))
            .where(Reservation.id == reservation_id)
        )
        return self.db.scalar(statement)

    def list(
        self,
        *,
        item_id: int | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Reservation]:
        statement = select(Reservation).options(joinedload(Reservation.item))
        if item_id is not None:
            statement = statement.where(Reservation.item_id == item_id)
        statement = statement.order_by(Reservation.id).offset(skip).limit(limit)
        return list(self.db.scalars(statement))

    def has_active_overlap(
        self,
        *,
        item_id: int,
        date_debut: date,
        date_fin: date,
    ) -> bool:
        statement = (
            select(Reservation.id)
            .where(
                Reservation.item_id == item_id,
                Reservation.statut == "active",
                Reservation.date_debut < date_fin,
                Reservation.date_fin > date_debut,
            )
            .limit(1)
        )
        return self.db.scalar(statement) is not None

    def add(self, reservation: Reservation) -> Reservation:
        self.db.add(reservation)
        self.db.flush()
        return reservation
