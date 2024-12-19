from common.producers import KafkaProducerService
from common.unit_of_work import UnitOfWork
from common.schemas import OrderDTO


class OrderPayUseCase:
    def __init__(self, uow: UnitOfWork, kafka_producer: KafkaProducerService):
        self._uow = uow
        self._producer = kafka_producer

    async def __call__(self, order_dto: OrderDTO):
        async with self._uow() as uow:
            order = await uow.orders.update_status(order_dto.id, 'new', 'paid')

            if order:
                await uow.commit()

                # log
                print(f'*** Заказ {order.id} оплачен ({order.status.value}) ***')

                order_dto = OrderDTO(id=order.id, status=order.status)
                await self._producer.send(
                    topic='paid',
                    message=order_dto.serialize()
                )


