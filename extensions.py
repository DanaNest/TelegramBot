import requests
import json
from config import currency


class APIException(Exception):
    pass


class CurrencyConvert:
    @staticmethod
    def get_price(quote: str , base: str, amount: str):
        if quote == base:
            raise APIException(f'Нельзя использовать одинаковые валюты!')

        try:
            quote_cur = currency[quote]
        except KeyError:
            raise APIException(f'Не удалось перевести валюту - {quote}!')


        try:
            base_cur = currency[base]
        except KeyError:
            raise APIException(f'Не удалось перевести валюту - {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Неправильно указано количество - {amount}')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/688b85181aab103d2ff74fa9/pair/{quote_cur}/{base_cur}/{amount}')
        total_base = json.loads(r.content)

        return total_base