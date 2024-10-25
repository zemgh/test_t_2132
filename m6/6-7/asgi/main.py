from catserver.server import CatServer

from app import WsgiApp
from routes import router

app = WsgiApp()
app.include_router(router)

if __name__ == '__main__':
    server = CatServer('127.0.0.1', 8000, app)
    server.run()