import asyncio
import sys

from dependency_injector.wiring import Provide, inject

from common.consumers import KafkaConsumersPool

from containers import ApplicationContainer
from usecase import OrderShippingUseCase


@inject
async def main(
        consumers_pool: KafkaConsumersPool = Provide[ApplicationContainer.infrastructure.kafka_consumers_pool],
        order_shipping_use_case: OrderShippingUseCase = Provide[ApplicationContainer.order_shipping_use_case]
):

    await consumers_pool.run(
        'paid',
        order_shipping_use_case,
        ApplicationContainer.kafka_consumer_deserialize
    )


if __name__ == '__main__':
    container = ApplicationContainer()
    container.config.from_yaml('common/config.yaml')
    container.wire(modules=[sys.modules[__name__]])
    asyncio.run(main())

