import os
import dataclasses


@dataclasses.dataclass
class KafkaConfig:
    brokers: str
    user: str
    password: str

    def config(self):
        return {
            "bootstrap_servers": self.brokers,
        }


@dataclasses.dataclass
class Config:
    kafka: KafkaConfig


def get_config():
    kafka = KafkaConfig(
        brokers=os.getenv("KAFKA_BROKERS") or "localhost",
        user=os.getenv("KAFKA_USER") or "",
        password=os.getenv("KAFKA_PASSWORD") or "",
    )
    return Config(kafka=kafka)
