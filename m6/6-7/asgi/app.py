import re
from typing import Optional, Union

from src.routes import Route
from src.exceptions import HttpException
from src.responses import ErrorResponse, BaseResponse


class AsgiApp:
    def __init__(self):
        self._routes: list[Route] = []


    async def __call__(self, scope, receive, send):
        try:
            method = scope['method']
            path = scope['path']
            response = await self._get_response(method, path)

        except HttpException as e:
            response = ErrorResponse(status_code=e.status_code, detail=e.detail)

        except Exception:
            response = ErrorResponse(status_code=500)

        finally:
            await send({
                'type': 'http.response.start',
                'status': response.status_code,
                'headers': response.headers
            })

            await send({
                'type': 'http.response.body',
                'body': response.body
            })


    def include_router(self, router):
        self._routes.extend(router.routes)


    async def _get_response(self, method: str, path: str) -> Union[BaseResponse, ErrorResponse]:
        route = self._get_route(method, path)
        params = route.params

        result = await route.handler(**params)

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





