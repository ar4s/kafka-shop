from fastapi import APIRouter
from core.models import ReservationEntity, ReservationRequest
from apps.dealer.constants import NAME

from ..dependencies import producer

router = APIRouter()


@router.post("/reserve")
async def reserve(id: int):
    await producer.reserve_car(ReservationRequest(car_id=id, dealer=NAME, type="request"))
    return {}
