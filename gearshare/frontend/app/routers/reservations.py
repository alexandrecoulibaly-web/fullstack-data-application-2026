from datetime import date
from typing import Annotated, Any

from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse, Response

from app.api_client import ApiError, api_client
from app.templating import templates

router = APIRouter()


def render_item_detail(
    request: Request,
    item_id: int,
    *,
    erreurs: list[str] | None = None,
    saisie: dict[str, Any] | None = None,
    message: str | None = None,
    status_code: int = 200,
) -> Response:
    item = api_client.get_item(item_id)
    reservations = api_client.list_reservations(item_id)
    return templates.TemplateResponse(
        request,
        "items/detail.html",
        {
            "item": item,
            "reservations": reservations,
            "erreurs": erreurs or [],
            "saisie": saisie or {},
            "message": message,
        },
        status_code=status_code,
    )


@router.post("/items/{item_id}/reservations")
def create_reservation_page(
    request: Request,
    item_id: int,
    date_debut: Annotated[date, Form()],
    date_fin: Annotated[date, Form()],
) -> Response:
    try:
        api_client.create_reservation(item_id, date_debut, date_fin)
    except ApiError as exc:
        if exc.status_code != 422:
            raise
        return render_item_detail(
            request,
            item_id,
            erreurs=exc.messages(),
            saisie={"date_debut": date_debut, "date_fin": date_fin},
            status_code=422,
        )
    return RedirectResponse(f"/items/{item_id}?reservation=ok", status_code=303)


@router.post("/reservations/{reservation_id}")
def cancel_reservation_page(
    request: Request,
    reservation_id: int,
    statut: Annotated[str, Form()],
    item_id: Annotated[int, Form()],
) -> Response:
    try:
        api_client.cancel_reservation(reservation_id, statut)
    except ApiError as exc:
        if exc.status_code != 409:
            raise
        return render_item_detail(
            request,
            item_id,
            message="Cette réservation est déjà annulée.",
            status_code=409,
        )
    return RedirectResponse(f"/items/{item_id}", status_code=303)
