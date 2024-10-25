import re
from typing import Optional, Union

from src.routes import Route
from src.exceptions import HttpException
from src.responses import ErrorResponse, BaseResponse


class WsgiApp:
    def __init__(self):
        self._routes: list[Route] = []


    def __call__(self, environ, start_response):
        try:
            method = environ['REQUEST_METHOD']
            path = environ['PATH_INFO']
            response = self._get_response(method, path)

        except HttpException as e:
            response = ErrorResponse(status_code=e.status_code, detail=e.detail)

        except Exception:
            response = ErrorResponse(status_code='500 INTERNAL SERVER ERROR')

        finally:
            start_response(response.status_code, response.headers)
            return [response.body]


    def include_router(self, router):
        self._routes.extend(router.routes)


    def _get_response(self, method: str, path: str) -> Union[BaseResponse, ErrorResponse]:
        route = self._get_route(method, path)
        params = route.params

        result = route.handler(**params)

        status_code = route.status_code
        response = route.response_cls(result, status_code)
        return response


    def _get_route(self, method, path) -> Route:
        for route in self._routes:

            match = self._match_path(route_path=route.path, request_path=path)
            if match:

                if route.method != method:
                    raise HttpException('405 Method Not Allowed')

                route.params = match.groupdict()
                return route

        raise HttpException('400 Bad Request')


    def _match_path(self, route_path: str, request_path: str) -> Optional[re.Match]:
        route_regex = re.sub(r'{(\w+)}', r'(?P<\1>[^/]+)', route_path)
        route_regex = f"^{route_regex}$"
        return re.match(route_regex, request_path)





