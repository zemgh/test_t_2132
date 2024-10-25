from typing import Callable


class Route:
    def __init__(self, path: str, method: str, handler: Callable, response_cls, status_code: str):
        self.path = path
        self.method = method
        self.params = None
        self.status_code = status_code
        self.handler = handler
        self.response_cls = response_cls


class Router:
    def __init__(self, prefix: str):
        self._prefix = prefix
        self._routes: list[Route] = []

    @property
    def routes(self) -> list[Route]:
        return self._routes

    def get(self, path: str, response_cls, status_code):

        def decorator(handler: Callable):
            route = Route(self._prefix + path, 'GET', handler, response_cls, status_code)
            self._routes.append(route)

            def wrapper(*args, **kwargs):
                return handler(*args, **kwargs)

            return wrapper
        return decorator
