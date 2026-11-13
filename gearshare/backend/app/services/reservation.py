from app.core.exceptions import BusinessConflict, ResourceNotFound
from app.models.reservation import Reservation
from app.repositories.item import ItemRepository
from app.repositories.reservation import ReservationRepository
from app.schemas.reservation import ReservationCreate


class ReservationService:
    def __init__(
        self,
        reservations: ReservationRepository,
        items: ItemRepository,
    ) -> None:
        self.reservations = reservations
        self.items = items

    def create(self, payload: ReservationCreate) -> Reservation:
        item = self.items.get(payload.item_id)
        if item is None:
            raise ResourceNotFound(f"Item {payload.item_id} introuvable")
        if not item.disponible:
            raise BusinessConflict("Cet item n'est pas disponible")
        if self.reservations.has_active_overlap(
            item_id=payload.item_id,
            date_debut=payload.date_debut,
            date_fin=payload.date_fin,
        ):
            raise BusinessConflict("Le créneau demandé est déjà réservé")

        return self.reservations.add(Reservation(**payload.model_dump()))

    def list(
        self,
        *,
        item_id: int | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> list[Reservation]:
        return self.reservations.list(item_id=item_id, skip=skip, limit=limit)

    def get(self, reservation_id: int) -> Reservation:
        reservation = self.reservations.get(reservation_id)
        if reservation is None:
            raise ResourceNotFound(f"Réservation {reservation_id} introuvable")
        return reservation

    def cancel(self, reservation_id: int) -> Reservation:
        reservation = self.get(reservation_id)
        if reservation.statut != "active":
            raise BusinessConflict("Cette réservation n'est plus active")
        reservation.statut = "annulee"
        return reservation
