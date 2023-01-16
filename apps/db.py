from typing import Dict, List
from collections import defaultdict

from core.models import (
    CarBrand, CarModel, CarEntity, EngineType, ReservationEntity)

car_models: List[CarModel] = [
    CarModel(
        engine=EngineType.petrol, brand=CarBrand.hyundai, name="i20", horse_power=100
    ),
    CarModel(engine=EngineType.diesel, brand=CarBrand.audi, name="A6", horse_power=240),
]

cars: Dict[int, CarEntity] = {}
reserved: Dict[str, List[CarEntity]] = defaultdict(list)

def add_car(car: CarEntity):
    cars[car.id] = car

def all_cars():
    return list(cars.values())

def add_car_model(model: CarModel):
    car_models.append(model)

def all_car_models():
    return car_models

def all_reserved():
    return list(reserved.values())

def reserve(entity: ReservationEntity):
    car = cars.get(entity.car_id)
    if car is None:
        return False
    reserved[entity.dealer].append(car)
    del cars[entity.car_id]
    return True
