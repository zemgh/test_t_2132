import json


class BaseResponse:
    pass


class JSONResponse(BaseResponse):
    def __init__(self, data: dict, status_code: int):
        self.status_code = status_code
        self.body = json.dumps(data).encode('utf-8')

        headers = [
            ('Content-type', 'application/json'),
            ('Content-Length', str(len(self.body)))
        ]
        self.headers = [(k.encode('utf-8'), v.encode('utf-8')) for k, v in headers]


class ErrorResponse:
    def __init__(self, status_code: int, detail: str = None):
        self.status_code = status_code
        self.body = self.get_body(status_code, detail)

        headers = [
            ('Content-type', 'application/json'),
            ('Content-Length', str(len(self.body)))
        ]
        self.headers = [(k.encode('utf-8'), v.encode('utf-8')) for k, v in headers]


    def get_body(self, status_code, detail) -> bytes:
        data = {'error': status_code}
        if detail:
            data['detail'] = detail

        return json.dumps(data).encode('utf-8')
