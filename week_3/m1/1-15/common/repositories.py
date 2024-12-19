from sqlalchemy import insert, Row, update, select

from models import Order


class DoesNotExist(Exception):
    pass


class OrderRepository:
    def __init__(self, session):
        self._session = session

    @staticmethod
    def _construct(row: Row) -> Order:
        if row is None:
            raise DoesNotExist

        return Order(
            id=row._mapping['id'],
            status=row._mapping['status']
        )

    async def create(self, data: dict) -> Order:
        query = insert(Order).values(**data).returning(Order.id, Order.status)

        result = await self._session.execute(query)
        row = result.fetchone()
        return self._construct(row)

    async def update_status(self, order_id: int, old_status: str, new_status: str):
        order = await self.get_order_with_lock(order_id, old_status)

        if order:
            updated_order = await self.set_status(order.id, new_status)
            return updated_order

    async def get_order_with_lock(self, order_id: int, status: str):
        query = (
            select(Order).
            where(Order.id == order_id, Order.status == status).
            with_for_update(skip_locked=True)
        )

        order = await self._session.scalar(query)
        return order

    async def set_status(self, order_id: int, status: str):
        query = (
            update(Order).
            where(Order.id == order_id).
            values(status=status).
            returning(Order.id, Order.status)
        )

        result = await self._session.execute(query)
        row = result.fetchone()
        return self._construct(row)

