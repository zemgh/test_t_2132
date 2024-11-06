class HttpException(Exception):
    def __init__(self, status_code: int, detail: str = None):
        self.status_code = status_code
        self.detail = detail

    def __str__(self):
        return f'{self.status_code}: {self.detail}'





