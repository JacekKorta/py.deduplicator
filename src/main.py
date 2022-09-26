import asyncio
import json
import logging
from datetime import timedelta

import aio_pika
from aio_pika.abc import AbstractRobustChannel, AbstractMessage
import redis
from redis import Redis

from config import get_settings
from models import Question

settings = get_settings()


async def my_publish(channel: AbstractRobustChannel, message_in: AbstractMessage):
    routing_key = settings.rabbit.output_routing_key
    exchange_name = settings.rabbit.output_exchange_name
    exchange = await channel.get_exchange(exchange_name)
    await exchange.publish(message_in, routing_key=routing_key)


def save_if_new(rdbc: Redis, question_id: int) -> bool:
    if rdbc.get(str(question_id)):
        return True
    rdbc.set(str(question_id), str(question_id), timedelta(hours=1))
    return False


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    connection = await aio_pika.connect_robust(settings.rabbitmq_uri)

    queue_name = settings.rabbit.input_queue_name

    async with connection:
        rdbc = redis.Redis()
        channel = await connection.channel()

        await channel.set_qos(prefetch_count=10)

        queue = await channel.get_queue(queue_name)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process(ignore_processed=True):
                    question = Question(**json.loads(message.body.decode()))
                    if not save_if_new(rdbc, question.question_id):
                        await my_publish(channel, message)
                    await message.reject()


if __name__ == "__main__":
    asyncio.run(main())
