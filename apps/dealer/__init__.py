import json
import asyncio
from typing import List

from apps.db import add_car
from fastapi import FastAPI
from core.kafka import get_topics, get_consumer
from core.models import CarEntity
from core.logging import get_logger
from apps.dealer.constants import NAME

from .routes import router
from ..dependencies import producer

logger = get_logger()

app = FastAPI(debug=True, title=f"{NAME} API")
topics = get_topics()
loop = asyncio.get_event_loop()
consumer = get_consumer(f"dealer-{NAME}")

app.include_router(router)

async def consume():
    logger.debug("Listen to topics")
    await consumer.start()
    try:
        async for msg in consumer:
            logger.info("msg %s", msg)
            handle_message(msg.topic, msg.value)
    finally:
        await consumer.stop()

def handle_message(topic, msg: bytes):
    try:
        if topic == topics.car_entity:
            new_car: CarEntity = CarEntity(**json.loads(msg))
            logger.info("Add a new car: id=%s", new_car.id)
            add_car(new_car)
        if topic == topics.reservation:
            logger.info(msg)
    except Exception as e:
        logger.error(e)


@app.on_event("shutdown")
async def unsubscribe():
    await consumer.stop()
    await producer.stop()


@app.on_event("startup")
async def start_server():
    loop.create_task(consume())
    await producer.start()
