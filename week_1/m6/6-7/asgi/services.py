from aiohttp import ClientSession
from src.exceptions import HttpException


class CurrencyService:
    _REQUEST_URL = 'https://api.exchangerate-api.com/v4/latest/'

    async def get_rates(self, currency: str):
        if len(currency) != 3:
            raise HttpException(
                status_code=400,
                detail='Currency len must be 3 characters'
            )

        async with ClientSession() as session:

            url = self._REQUEST_URL + currency
            async with session.get(url) as response:

                if response.status == 200:
                    data = await response.json()
                    return data['rates']

                if response.status == 404:
                    raise HttpException(
                        status_code=404,
                        detail='Unsupported currency code'
                    )

                raise HttpException(
                    status_code=503,
                    detail='Try again later'
                )


