from dependency_injector import containers, providers

from common.containers import InfrastructureContainer
from common.schemas import OrderDTO

from usecase import OrderShippingUseCase


class ApplicationContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    infrastructure = providers.Container[InfrastructureContainer](
        InfrastructureContainer,
        config=config
    )

    order_shipping_use_case = providers.Singleton[OrderShippingUseCase](
        OrderShippingUseCase,
        uow=infrastructure.unit_of_work,
        kafka_producer=infrastructure.kafka_producer
    )

    kafka_consumer_deserialize = OrderDTO.deserialize