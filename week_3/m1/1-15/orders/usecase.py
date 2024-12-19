from common.schemas import OrderDTO
from common.producers import KafkaProducerService
from common.models import Order
from common.unit_of_work import UnitOfWork


class OrderCreateUseCase:
    def __init__(self, uow: UnitOfWork, kafka_producer: KafkaProducerService):
        self._uow = uow
        self._producer = kafka_producer

    async def __call__(self, order_data: dict) -> Order:
        async with self._uow() as uow:
            order = await uow.orders.create(order_data)
            await uow.commit()

            # log
            print(f'*** Заказ {order.id} создан ({order.status.value}) ***')

            order_dto = OrderDTO(id=order.id, status=order.status)
            await self._producer.send(
                topic='new',
                message=order_dto.serialize()
            )

            return order
