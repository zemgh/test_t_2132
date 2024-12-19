import enum

from sqlalchemy import Column, Integer, Enum
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class OrderStatus(enum.Enum):
    new = 'new'
    paid = 'paid'
    shipping = 'shipping'
    delivered = 'delivered'


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.new)