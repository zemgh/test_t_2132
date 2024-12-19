import asyncio
import sys

import uvicorn
from aiokafka import AIOKafkaProducer
from dependency_injector.wiring import inject, Provide

from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse

from common.schemas import OrderCreateSchema

from usecase import OrderCreateUseCase
from containers import ApplicationContainer

app = FastAPI()

PRODUCER_TOPIC = 'new'


@app.post('/orders/create', status_code=201)
@inject
async def create_order(
        order_data: OrderCreateSchema,
        order_create_use_case: OrderCreateUseCase = Depends(
            Provide[ApplicationContainer.order_create_use_case]
        )
):

    order = await order_create_use_case(order_data.dict())

    return {
        'id': order.id,
        'status': order.status,
    }


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            'message': 'Server Error',
            'request_url': str(request.url),
            'error': str(exc)
        }
    )


async def producer_test():
    p = AIOKafkaProducer(
        bootstrap_servers='127.0.0.1:9092',
        acks='all',
        linger_ms=0,
        enable_idempotence=False
    )
    await p.start()
    await p.send(topic='new', value=b'test')
    await p.stop()

if __name__ == '__main__':
    container = ApplicationContainer()
    container.config.from_yaml('common/config.yaml')
    container.wire(modules=[sys.modules[__name__]])
    # asyncio.run(producer_test())
    # отрабатывает коректно
    uvicorn.run(app, port=8000)

