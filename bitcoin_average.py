# -*- coding: utf-8 -*-
import os

import decimal

import datetime
from bitcoinaverage import RestfulClient
from typing import List

from base import AbstractDataSource, Symbol


class BitcoinAverage(AbstractDataSource):
    secret_key = os.environ['BITCOIN_AVERAGE_SECRET_KEY']
    public_key = os.environ['BITCOIN_AVERAGE_PUBLIC_KEY']
    client = RestfulClient(secret_key, public_key)

    @classmethod
    def symbols(cls) -> List[str]:
        """返回支持的加密货币列表"""
        symbols = cls.client.all_symbols()
        return list(set(symbols['crypto']['symbols']))

    @classmethod
    def historical_data(cls, symbol: str, start_day: datetime.datetime, end_day: datetime.datetime) -> List[Symbol]:
        """返回支持的加密货币列表"""
        currency = cls.get_currency_from_symbol(symbol)
        all_historical_data = cls.client.history_global(symbol)
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

    @classmethod
    def get_currency_from_symbol(cls, symbol):
        return symbol[3:]