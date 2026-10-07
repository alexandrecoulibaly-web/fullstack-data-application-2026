from datetime import date

import pytest
from pydantic import ValidationError

from app.schemas.reservation import ReservationCreate


ITEM = {
    "titre": "Appareil photo",
    "description": None,
    "tarif_jour": 25.5,
    "disponible": True,
}
RESERVATION = {
    "item_id": 1,
    "date_debut": "2026-10-10",
    "date_fin": "2026-10-12",
}


@pytest.fixture()
def reservation_active(client):
    item_response = client.post("/items", json=ITEM)
    assert item_response.status_code == 201

    response = client.post("/reservations", json=RESERVATION)
    assert response.status_code == 201
    return response.json()


def test_creer_reservation_retourne_une_reservation_active(client):
    client.post("/items", json=ITEM)

    response = client.post("/reservations", json=RESERVATION)

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["item_id"] == 1
    assert body["date_debut"] == RESERVATION["date_debut"]
    assert body["date_fin"] == RESERVATION["date_fin"]
    assert body["statut"] == "active"


def test_relire_reservation_creee_retourne_ses_donnees(client, reservation_active):
    response = client.get(f"/reservations/{reservation_active['id']}")

    assert response.status_code == 200
    assert response.json() == reservation_active


def test_creer_reservation_avec_item_inexistant_est_accepte_par_le_contrat_actuel(
    client,
):
    response = client.post("/reservations", json={**RESERVATION, "item_id": 999})

    assert response.status_code == 201
    assert response.json()["item_id"] == 999


def test_lire_reservation_inexistante_retourne_404(client):
    response = client.get("/reservations/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Réservation 999 introuvable"


def test_lister_reservations_filtre_par_item_et_limite(client, reservation_active):
    client.post(
        "/reservations",
        json={**RESERVATION, "item_id": 2, "date_debut": "2026-11-01", "date_fin": "2026-11-03"},
    )

    response = client.get(
        "/reservations", params={"item_id": reservation_active["item_id"], "limit": 1}
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == reservation_active["id"]


@pytest.mark.parametrize(
    ("payload", "field"),
    [
        ({**RESERVATION, "item_id": 0}, "item_id"),
        ({**RESERVATION, "date_debut": "not-a-date"}, "date_debut"),
    ],
)
def test_creer_reservation_payload_invalide_retourne_422(client, payload, field):
    response = client.post("/reservations", json=payload)

    assert response.status_code == 422
    assert any(error["loc"][-1] == field for error in response.json()["detail"])


def test_annuler_reservation_existante_change_son_statut(client, reservation_active):
    response = client.post(f"/reservations/{reservation_active['id']}/annuler")

    assert response.status_code == 200
    assert response.json()["statut"] == "annulee"
    assert (
        client.get(f"/reservations/{reservation_active['id']}").json()["statut"]
        == "annulee"
    )


def test_annuler_reservation_inexistante_retourne_404(client):
    response = client.post("/reservations/999/annuler")

    assert response.status_code == 404
    assert response.json()["detail"] == "Réservation 999 introuvable"


def test_annuler_deux_fois_une_reservation_retourne_409(client, reservation_active):
    client.post(f"/reservations/{reservation_active['id']}/annuler")

    response = client.post(f"/reservations/{reservation_active['id']}/annuler")

    assert response.status_code == 409
    assert response.json()["detail"] == "Réservation 1 déjà annulée"


def test_reservation_create_refuse_date_fin_anterieure_ou_egale():
    for date_fin in (date(2026, 10, 10), date(2026, 10, 9)):
        with pytest.raises(ValidationError) as exc_info:
            ReservationCreate(
                item_id=1, date_debut=date(2026, 10, 10), date_fin=date_fin
            )

        assert "date_fin" in str(exc_info.value)
