# -*- coding: utf-8 -*-

import datetime
import decimal
from bitcoinaverage import RestfulClient
from typing import List

from coin_data.base import AbstractDataSource, Symbol


class BitcoinAverage(AbstractDataSource):

    def __init__(self, secret_key, public_key):
        self.client = RestfulClient(secret_key, public_key)

    def symbols(self) -> List[str]:
        """返回支持的加密货币列表"""
        symbols = self.client.all_symbols()
        return list(set(symbols['crypto']['symbols']))

    def historical_data(self, symbol: str, start_day: datetime.datetime, end_day: datetime.datetime) -> List[Symbol]:
        """返回支持的加密货币列表"""
        currency = self.get_currency_from_symbol(symbol)
        all_historical_data = self.client.history_global(symbol)
        historical_data = []
        for doc in all_historical_data:
            symbol_time = datetime.datetime.strptime(doc['time'], "%Y-%m-%d %H:%M:%S")
            if start_day <= symbol_time <= end_day:
                symbol_obj = Symbol(
                    name=symbol,
                    time=symbol_time,
                    average_price=decimal.Decimal(doc['average']),
                    currency=currency
                )
                historical_data.append(symbol_obj)
        return historical_data

    def get_currency_from_symbol(self, symbol):
        return symbol[3:]
