from common.schemas import OrderDTO
from common.unit_of_work import UnitOfWork


class OrderNotificationsUseCase:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def __call__(self, order_dto: OrderDTO):
        async with self._uow() as uow:
            order = await uow.orders.update_status(order_dto.id, 'shipping', 'delivered')

            if order:
                await uow.commit()

                # log
                print(f'*** Юзвер, твой заказ {order.id} доставлен ({order.status.value}) ***')

