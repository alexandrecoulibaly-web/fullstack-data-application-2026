# app/api_client.py
import os
from datetime import date
from typing import Any

import httpx


class ApiError(Exception):
    """Erreur renvoyée par le backend, ou backend injoignable."""

    def __init__(self, status_code: int, detail: Any) -> None:
        super().__init__(f"{status_code}: {detail}")
        self.status_code = status_code
        self.detail = detail

    def messages(self) -> list[str]:
        """Renvoie la liste des messages d'erreur à afficher à l'utilisateur."""
        if isinstance(self.detail, str):
            return [self.detail]

        if isinstance(self.detail, list):
            messages: list[str] = []
            for error in self.detail:
                if isinstance(error, dict) and "loc" in error and "msg" in error:
                    field = error["loc"][-1]
                    messages.append(f"{field}: {error['msg']}")
                else:
                    messages.append(str(error))
            return messages

        if isinstance(self.detail, dict) and "msg" in self.detail:
            return [str(self.detail["msg"])]

        return [str(self.detail)]




class ApiClient:
    """Porte d'entrée unique du frontend vers l'API du backend."""

    def __init__(self, base_url: str, timeout: float = 10) -> None:
        self._http = httpx.Client(base_url=base_url, timeout=timeout)

    def _send(self, method: str, url: str, **kwargs: Any) -> Any:
        try:
            response = self._http.request(method, url, **kwargs)
        except httpx.RequestError as exc:
            raise ApiError(503, "Le service est momentanément indisponible.") from exc
        if response.is_error:
            try:
                detail = response.json().get("detail")
            except ValueError:
                detail = response.text
            raise ApiError(response.status_code, detail)
        return response.json() if response.content else None

    def list_items(self, limit: int = 20) -> list[dict[str, Any]]:
        return self._send("GET", "/items", params={"limit": limit})

    def get_item(self, item_id: int) -> dict[str, Any]:
        return self._send("GET", f"/items/{item_id}")

    def list_reservations(self, item_id: int) -> list[dict[str, Any]]:
        return self._send("GET", "/reservations", params={"item_id": item_id})

    def create_item(
        self,
        titre: str,
        description: str | None,
        tarif_jour: float,
        disponible: bool = True,
    ) -> dict[str, Any]:
        return self._send(
            "POST",
            "/items",
            json={
                "titre": titre,
                "description": description,
                "tarif_jour": tarif_jour,
                "disponible": disponible,
            },
        )

    def create_reservation(self, item_id: int, date_debut: date, date_fin: date) -> dict[str, Any]:
        return self._send(
            "POST",
            "/reservations",
            json={"item_id": item_id, "date_debut": date_debut.isoformat(), "date_fin": date_fin.isoformat()},
        )

    def cancel_reservation(
        self, reservation_id: int, statut: str = "annulee"
    ) -> dict[str, Any]:
        return self._send(
            "PATCH",
            f"/reservations/{reservation_id}",
            json={"statut": statut},
        )


api_client = ApiClient(base_url=os.environ["API_BASE_URL"])