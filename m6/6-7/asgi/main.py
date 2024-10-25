import asyncio

from acatsserver.server import ACatServer
from app import AsgiApp
from routes import router

app = AsgiApp()
app.include_router(router)

if __name__ == '__main__':
    server = ACatServer('127.0.0.1', 8000, app)
    asyncio.run(server.run())
