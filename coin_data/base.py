# -*- coding: utf-8 -*-
import datetime
import decimal
from typing import List


class Symbol:

    def __init__(self, name: str, time: datetime.datetime, average_price: decimal.Decimal, currency: str):
        self.name = name
        self.time = time
        self.average_price = average_price
        self.currency = currency


class AbstractDataSource:

    def symbols(self) -> List[str]:
        """返回支持的加密货币列表"""
        raise NotImplementedError

    def historical_data(self, symbol: str, start_day: datetime.datetime, end_day: datetime.datetime) -> List[Symbol]:
        """返回 symbol 在 [start_day, end_day] 的数据"""
        raise NotImplementedError
