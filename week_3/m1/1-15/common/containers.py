from typing import Callable

from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker

from .consumers import KafkaConsumersPool
from .producers import KafkaProducerService
from .unit_of_work import UnitOfWork

# Тут должно быть 3 контейнера?

class InfrastructureContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    async_engine = providers.Singleton[AsyncEngine](
        create_async_engine,
        url=config.infrastructure.db.url
    )

    session_factory: Callable[..., AsyncSession] = providers.Factory(
        sessionmaker, async_engine, expire_on_commit=False, class_=AsyncSession
    )

    unit_of_work = providers.Singleton[UnitOfWork](
        UnitOfWork,
        session_factory=session_factory
    )

    kafka_producer = providers.Singleton[KafkaProducerService](
        KafkaProducerService,
        config=config.infrastructure.kafka.producer.config
    )

    kafka_consumers_pool = providers.Singleton[KafkaConsumersPool](
        KafkaConsumersPool,
        config=config.infrastructure.kafka.consumer.config
    )
