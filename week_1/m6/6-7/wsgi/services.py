import requests

from src.exceptions import HttpException


class CurrencyService:
    _REQUEST_URL = 'https://api.exchangerate-api.com/v4/latest/'

    def get_rates(self, currency: str):
        if len(currency) != 3:
            raise HttpException(
                status_code='404 Not Found',
                detail='Currency len must be 3 characters'
            )

        url = self._REQUEST_URL + currency
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data['rates']

        if response.status_code == 404:
            raise HttpException(
                status_code='400 Bad Request',
                detail='Unsupported currency code'
            )

        raise HttpException(
            status_code='503 Service Unavailable',
            detail='Try again later'
        )
