import json
import uuid
from typing import Union

from core import get_config
# from confluent_kafka import Consumer, Producer
from aiokafka import AIOKafkaConsumer as Consumer
from aiokafka import AIOKafkaProducer as Producer
from pydantic import BaseModel
from core.models import (
    CarModel, CarEntity, ReservationEntity, ReservationRequest,
    ReservationConfirmationEntity)


class Topics(BaseModel):
    car_entity: str
    car_model: str
    reservation: str


def get_topics():
    return Topics(car_entity=f"car-entity", car_model=f"car-model", reservation="reservation")


class ProducerFacade:
    _p: Producer
    _topics: Topics

    def __init__(self, producer: Producer):
        self._p = producer
        self._topics = get_topics()

    async def start(self):
        await self._p.start()

    async def stop(self):
        await self._p.stop()

    async def car_model(self, model: CarModel):
        await self._p.send(self._topics.car_model, model.json().encode("utf-8"))

    async def car_entity(self, entity: CarEntity):
        await self._p.send(self._topics.car_entity, entity.json().encode("utf-8"))

    async def reserve_car(self, entity: Union[ReservationRequest, ReservationConfirmationEntity]):
        return await self._p.send_and_wait(self._topics.reservation, entity.json().encode('utf-8'))

def get_producer():
    config = get_config()
    producer = Producer(
        **config.kafka.config(),
    )
    return ProducerFacade(producer)


def get_consumer(name: str):
    config = get_config()
    topics = get_topics()

    return Consumer(
        topics.car_entity,
        topics.car_model,
        topics.reservation,
        **{**config.kafka.config(), "group_id": name},
    )
