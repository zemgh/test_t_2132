from dependency_injector import containers, providers

from common.containers import InfrastructureContainer

from usecase import OrderCreateUseCase


class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    infrastructure = providers.Container[InfrastructureContainer](
        InfrastructureContainer,
        config=config
    )

    order_create_use_case = providers.Singleton[OrderCreateUseCase](
        OrderCreateUseCase,
        uow=infrastructure.unit_of_work,
        kafka_producer=infrastructure.kafka_producer
    )