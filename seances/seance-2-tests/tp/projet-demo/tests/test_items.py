import pytest
from pydantic import ValidationError

from app.schemas.item import ItemCreate, ItemUpdate


ITEM = {
    "titre": "Appareil photo",
    "description": "Boîtier hybride",
    "tarif_jour": 25.5,
    "disponible": True,
}


def create_item(client, payload=None):
    return client.post("/items", json=payload or ITEM)


def test_creer_item_retourne_item_complet_avec_identifiant(client):
    response = create_item(client)

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["titre"] == ITEM["titre"]
    assert body["description"] == ITEM["description"]
    assert body["tarif_jour"] == ITEM["tarif_jour"]
    assert body["disponible"] is True


@pytest.mark.parametrize(
    ("payload", "field"),
    [
        ({**ITEM, "titre": "ab"}, "titre"),
        ({**ITEM, "titre": "a" * 121}, "titre"),
        ({**ITEM, "tarif_jour": 0}, "tarif_jour"),
        ({**ITEM, "tarif_jour": -1}, "tarif_jour"),
    ],
)
def test_creer_item_payload_invalide_retourne_422(client, payload, field):
    response = create_item(client, payload)

    assert response.status_code == 422
    assert any(error["loc"][-1] == field for error in response.json()["detail"])


def test_lire_item_existant(client):
    created = create_item(client).json()

    response = client.get(f"/items/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]
    assert response.json()["titre"] == ITEM["titre"]


def test_lire_item_inexistant_retourne_404(client):
    response = client.get("/items/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Item 999 introuvable"


def test_lister_items_avec_pagination_et_recherche(client):
    create_item(client, {**ITEM, "titre": "Appareil photo"})
    create_item(client, {**ITEM, "titre": "Trépied photo"})
    create_item(client, {**ITEM, "titre": "Sac de transport"})

    response = client.get("/items", params={"skip": 1, "limit": 1, "q": "photo"})

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["titre"] == "Trépied photo"


def test_lister_items_filtre_sur_la_disponibilite(client):
    create_item(client, {**ITEM, "titre": "Disponible", "disponible": True})
    create_item(client, {**ITEM, "titre": "Indisponible", "disponible": False})

    response = client.get("/items", params={"disponible": False})

    assert response.status_code == 200
    assert [item["titre"] for item in response.json()] == ["Indisponible"]


@pytest.mark.parametrize(
    "params",
    [{"skip": -1}, {"limit": 0}, {"limit": 101}],
)
def test_lister_items_parametres_invalides_retourne_422(client, params):
    response = client.get("/items", params=params)

    assert response.status_code == 422
    assert "query" in response.json()["detail"][0]["loc"]


def test_remplacer_item_modifie_tous_les_champs(client):
    created = create_item(client).json()
    replacement = {
        "titre": "Objectif grand angle",
        "description": "Objectif 24 mm",
        "tarif_jour": 40,
        "disponible": False,
    }

    response = client.put(f"/items/{created['id']}", json=replacement)

    assert response.status_code == 200
    assert response.json() == {"id": created["id"], **replacement}


def test_remplacer_item_inexistant_retourne_404(client):
    response = client.put("/items/999", json=ITEM)

    assert response.status_code == 404
    assert response.json()["detail"] == "Item 999 introuvable"


def test_modifier_partiellement_item_conserve_les_champs_absents(client):
    created = create_item(client).json()

    response = client.patch(
        f"/items/{created['id']}", json={"tarif_jour": 30, "disponible": False}
    )

    assert response.status_code == 200
    assert response.json()["titre"] == ITEM["titre"]
    assert response.json()["description"] == ITEM["description"]
    assert response.json()["tarif_jour"] == 30
    assert response.json()["disponible"] is False


def test_modifier_partiellement_item_inexistant_retourne_404(client):
    response = client.patch("/items/999", json={"tarif_jour": 30})

    assert response.status_code == 404
    assert response.json()["detail"] == "Item 999 introuvable"


@pytest.mark.parametrize(
    ("payload", "field"),
    [({"titre": "ab"}, "titre"), ({"tarif_jour": 0}, "tarif_jour")],
)
def test_modifier_partiellement_item_payload_invalide_retourne_422(
    client, payload, field
):
    created = create_item(client).json()

    response = client.patch(f"/items/{created['id']}", json=payload)

    assert response.status_code == 422
    assert any(error["loc"][-1] == field for error in response.json()["detail"])


def test_supprimer_item_existant_retourne_204_et_le_rend_inaccessible(client):
    created = create_item(client).json()

    response = client.delete(f"/items/{created['id']}")

    assert response.status_code == 204
    assert response.content == b""
    assert client.get(f"/items/{created['id']}").status_code == 404


def test_supprimer_item_inexistant_retourne_404(client):
    response = client.delete("/items/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Item 999 introuvable"


def test_item_create_refuse_un_titre_trop_court():
    with pytest.raises(ValidationError) as exc_info:
        ItemCreate(titre="ab", tarif_jour=10)

    assert "titre" in str(exc_info.value)


def test_item_update_accepte_un_payload_vide():
    update = ItemUpdate()

    assert update.model_dump(exclude_unset=True) == {}
