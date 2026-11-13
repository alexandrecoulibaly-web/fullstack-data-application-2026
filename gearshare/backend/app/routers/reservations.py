from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status

from app.api.deps import DbSession
from app.repositories.item import ItemRepository
from app.repositories.reservation import ReservationRepository
from app.schemas.reservation import ReservationCreate, ReservationRead, ReservationUpdate
from app.services.reservation import ReservationService

router = APIRouter(prefix="/reservations", tags=["reservations"])


def get_reservation_service(db: DbSession) -> ReservationService:
    return ReservationService(ReservationRepository(db), ItemRepository(db))


ReservationServiceDependency = Annotated[
    ReservationService, Depends(get_reservation_service)
]


@router.post("", response_model=ReservationRead, status_code=status.HTTP_201_CREATED)
def create_reservation(
    payload: ReservationCreate, service: ReservationServiceDependency
) -> ReservationRead:
    return service.create(payload)


@router.get("", response_model=list[ReservationRead])
def list_reservations(
    service: ReservationServiceDependency,
    item_id: int | None = Query(default=None, ge=1),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
) -> list[ReservationRead]:
    return service.list(item_id=item_id, skip=skip, limit=limit)


@router.get("/{reservation_id}", response_model=ReservationRead)
def get_reservation(
    service: ReservationServiceDependency,
    reservation_id: int = Path(ge=1),
) -> ReservationRead:
    return service.get(reservation_id)


@router.patch("/{reservation_id}", response_model=ReservationRead)
def update_reservation(
    payload: ReservationUpdate,
    service: ReservationServiceDependency,
    reservation_id: int = Path(ge=1),
) -> ReservationRead:
    return service.cancel(reservation_id)
