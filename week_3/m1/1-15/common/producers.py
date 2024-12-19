import logging

from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaError


class KafkaProducerService:
    def __init__(self, config: dict):
        self._producer = AIOKafkaProducer(**config)

    async def send(self, topic: str, message: bytes):
        try:
            if not self._producer._closed:
                await self._producer.start()

            callback = await self._producer.send_and_wait(
                topic=topic,
                value=message
            )

            # log
            print(f'[Producer] sent: {callback.topic}/{callback.partition}')

            await self._producer.flush()

        except KafkaError as e:
            logging.error(f'[Producer] encountered a Kafka error: {e}')

        except Exception as e:
            logging.error(f'[Producer] encountered an error: {e}')
