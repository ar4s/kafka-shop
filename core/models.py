from enum import Enum
from typing import Literal, Union
from uuid import UUID

from pydantic import BaseModel


class EngineType(str, Enum):
    ev = "electrical"
    diesel = "diesel"
    petrol = "petrol"


class CarBrand(str, Enum):
    audi = "Audi"
    hyundai = "Hyundai"
    ford = "Ford"


class CarModel(BaseModel):
    engine: EngineType
    brand: CarBrand
    name: str
    horse_power: int


class CarEntity(BaseModel):
    id: int
    car: CarModel


class ReservationEntity(BaseModel):
    car_id: int
    dealer: str
    type: Literal["request", "confirmation"]

class ReservationRequest(ReservationEntity):
    pass

class ReservationConfirmationEntity(ReservationEntity):
    success: bool
