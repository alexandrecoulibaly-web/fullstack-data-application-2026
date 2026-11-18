from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ReservationCreate(BaseModel):
    item_id: int = Field(ge=1)
    borrower_id: int = Field(ge=1)
    date_debut: date
    date_fin: date

    @model_validator(mode="after")
    def validate_dates(self) -> "ReservationCreate":
        if self.date_fin <= self.date_debut:
            raise ValueError("la date de fin de réservation doit être postérieure à la date de début")
        return self


class ReservationUpdate(BaseModel):
    statut: Literal["annulee"]


class ItemSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titre: str


class ReservationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    item_id: int
    borrower_id: int
    date_debut: date
    date_fin: date
    statut: str
    item: ItemSummary
