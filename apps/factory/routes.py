from fastapi import APIRouter
from core.models import CarModel, CarEntity

from ..db import add_car, all_cars, add_car_model, all_car_models
from ..dependencies import producer

router = APIRouter()


@router.get("/cars")
async def index():
    return {"cars": all_cars()}


@router.get("/models")
async def index_models():
    return {"models": all_car_models()}


@router.post("/car/model")
async def create_car_model(car_model: CarModel):
    add_car_model(car_model)
    await producer.car_model(car_model)
    return {"status": "ok"}


@router.post("/car/entity")
async def create_car_entity(car_entity: CarEntity):
    add_car(car_entity)
    await producer.car_entity(car_entity)
    return {"status": "ok"}
