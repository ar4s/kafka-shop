import os
import json
import asyncio
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from core.kafka import get_topics, get_consumer
from core.models import CarEntity, ReservationEntity
from core.logging import get_logger

name = int(os.getenv("PORT") or "7201") - 7200
logger = get_logger()
app = FastAPI(debug=True, title=f"Statistics {name} API")
cars: List[CarEntity] = []
topics = get_topics()
loop = asyncio.get_event_loop()
consumer = get_consumer(f"statistics-{name}")


@app.on_event("startup")
async def listen_topic():
    loop.create_task(consume())


@app.on_event("shutdown")
async def unsubscribe():
    await consumer.stop()


async def consume():
    logger.debug("Listen to topics")
    await consumer.start()
    try:
        async for msg in consumer:
            handle_message(topics.car_entity, msg.value)
    finally:
        await consumer.stop()


def handle_message(topic, msg: bytes):
    if topic == topics.car_entity:
        new_car: CarEntity = CarEntity(**json.loads(msg))
        logger.info("Add a new car: id=%s", new_car.id)
        cars.append(new_car)

    if topic == topics.reservation:
        reservation = ReservationEntity(**json.loads(msg))
        logger.info("Reservation, %s", reservation)


class CarsResponse(BaseModel):
    cars: List[CarEntity]


@app.get("/cars")
async def index() -> CarsResponse:
    return CarsResponse(cars=cars)
