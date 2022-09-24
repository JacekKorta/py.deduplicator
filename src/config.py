from functools import lru_cache
from pydantic import BaseSettings, Field


class RedisSettings(BaseSettings):
    host: str = Field("localhost", env="REDIS_HOST")
    port: int = Field(6379, env="REDIS_PORT")
    key_ttl: int = Field(3600, env="REDIS_KEY_TTL")

    class Config:
        env_file = ".env"


class RabbitMQSettings(BaseSettings):
    user: str = Field("guest", env="RABBITMQ_USER")
    password: str = Field("guest", env="RABBITMQ_PASSWORD")
    host: str = Field("localhost", env="RABBITMQ_HOST")
    port: int = Field(5672, env="RABBITMQ_PORT")
    vhost: str = Field(..., env="RABBITMQ_VHOST")
    input_queue_name: str = Field(..., env="RABBITMQ_INPUT_QUEUE")
    output_exchange_name: str = Field(..., env="RABBITMQ_OUTPUT_EXCHANGE")
    output_routing_key: str = Field(..., env="RABBITMQ_OUTPUT_ROUTING_KEY")

    class Config:
        env_file = ".env"


class Settings(BaseSettings):
    rabbit: RabbitMQSettings = RabbitMQSettings()
    redis: RedisSettings = RedisSettings()

    class Config:
        env_file = ".env"

    @property
    def rabbitmq_uri(self):
        return (
            f"amqp://{self.rabbit.user}:{self.rabbit.password}@"
            f"{self.rabbit.host}:{self.rabbit.port}/{self.rabbit.vhost}"
        )


@lru_cache()
def get_settings() -> Settings:
    return Settings()
