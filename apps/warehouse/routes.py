from fastapi import APIRouter
from core.models import CarModel, CarEntity

from ..db import add_car, all_cars, all_reserved, add_car_model, all_car_models
from ..dependencies import producer

router = APIRouter()


@router.get("/stock")
async def stock():
    return {"cars": all_cars()}

@router.get("/reserved")
async def reserved():
    return {"cars": all_reserved()}

