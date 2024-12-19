import asyncio
import logging
from typing import Callable

from aiokafka import AIOKafkaConsumer, TopicPartition
from aiokafka.errors import KafkaError
from confluent_kafka.admin import AdminClient

from schemas import BaseDTO


class AsyncKafkaConsumer:
    def __init__(self,
                 config: dict,
                 topic: str,
                 partition_key: int,
                 use_case: Callable,
                 deserialize_cls: BaseDTO
                 ):

        self._consumer = AIOKafkaConsumer(value_deserializer=deserialize_cls, **config)
        self._topic = topic
        self._partition_key = partition_key
        self._use_case = use_case

    def _assign_partition(self):
        partition = TopicPartition(self._topic, self._partition_key)
        self._consumer.assign([partition])

    async def consume(self):
        await self._consumer.start()

        try:
            self._assign_partition()
            # log
            print(f'Start polling partition: {self._topic}/{self._partition_key}')

            async for message in self._consumer:
                try:
                    # log
                    print(f'[Consumer] message: {message.value}')
                    await self._use_case(message.value)

                except KafkaError as e:
                    logging.error(f'[Consumer] encountered a Kafka error: {e}')

                except Exception as e:
                    logging.error(f'[Consumer] encountered an error: {e}')

                finally:
                    await self._consumer.commit()

        finally:
            await self._consumer.stop()


class KafkaConsumersPool:
    def __init__(self, config: dict):
        self._config = config
        self._admin = AdminClient({
            k.replace('_', '.'): v for k, v in config.items()
        })

    def _get_partitions_keys(self, topic):
        return self._admin.list_topics(topic).topics[topic].partitions.keys()

    async def run(self, topic: str, use_case: Callable, deserialize_cls: BaseDTO):
        partitions = self._get_partitions_keys(topic)
        consumers = [AsyncKafkaConsumer(self._config, topic, key, use_case, deserialize_cls) for key in partitions]

        tasks = [consumer.consume() for consumer in consumers]
        await asyncio.gather(*tasks)
