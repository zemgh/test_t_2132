from src.routes import Router
from src.responses import JSONResponse

from services import CurrencyService

router = Router('')


@router.get('/{currency}', response_cls=JSONResponse, status_code=200)
async def get_currency(currency: str) -> dict:
    service = CurrencyService()
    rates = await service.get_rates(currency)
    return rates
