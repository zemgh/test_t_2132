from src.exceptions import HttpException
import requests


class CurrencyService:
    def get_rates(self, currency: str):
        if len(currency) != 3:
            raise HttpException(
                status_code='400 Bad Request',
                detail='Currency len must be 3 characters'
            )

        url = 'https://api.exchangerate-api.com/v4/latest/' + currency
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data['rates']

        if response.status_code == 404:
            raise HttpException(
                status_code='404 Not Found',
                detail='Unsupported currency code'
            )

        raise HttpException(
            status_code='503 Service Unavailable',
            detail='Try again later'
        )


