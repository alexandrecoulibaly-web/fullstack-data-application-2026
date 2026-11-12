from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ItemCreate(BaseModel):
    owner_id: int = Field(ge=1)
    titre: str = Field(min_length=3, max_length=120)
    description: str | None = Field(default=None, max_length=1000)
    tarif_jour: Decimal = Field(gt=0, max_digits=8, decimal_places=2)
    disponible: bool = True


class ItemUpdate(BaseModel):
    titre: str | None = Field(default=None, min_length=3, max_length=120)
    description: str | None = Field(default=None, max_length=1000)
    tarif_jour: Decimal | None = Field(
        default=None, gt=0, max_digits=8, decimal_places=2
    )
    disponible: bool | None = None


class OwnerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    display_name: str


class ItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    titre: str
    description: str | None
    tarif_jour: Decimal
    disponible: bool
    owner: OwnerRead
