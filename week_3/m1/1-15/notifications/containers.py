from dependency_injector import containers, providers

from common.containers import InfrastructureContainer
from common.schemas import OrderDTO

from usecase import OrderNotificationsUseCase


class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    infrastructure = providers.Container[InfrastructureContainer](
        InfrastructureContainer,
        config=config
    )

    order_notifications_use_case = providers.Singleton[OrderNotificationsUseCase](
        OrderNotificationsUseCase,
        uow=infrastructure.unit_of_work
    )

    kafka_consumer_deserialize = OrderDTO.deserialize
