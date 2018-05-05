# -*- coding: utf-8 -*-
import datetime
import decimal
from typing import List


class Coin:
    DATE_FORMAT = '%Y-%m-%d'

    def __init__(self,
                 name: str,
                 symbol: str,
                 time: datetime.datetime,
                 open: decimal.Decimal,
                 high: decimal.Decimal,
                 low: decimal.Decimal,
                 close: decimal.Decimal,
                 volume: decimal.Decimal,
                 market_cap: decimal.Decimal,
                 currency: str = 'USD'
                 ):
        """
        :param name: 全名，比如 BitCoin
        :param symbol: 代号，比如 BTC
        :param time: UTC 时间
        :param open: 开盘价
        :param high: 最高价
        :param low: 最低价
        :param close: 闭盘价
        :param volume: 成交量
        :param market_cap: market_cap
        :param currency: 货币单位
        """
        self.name = name
        self.symbol = symbol
        self.time = time
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.market_cap = market_cap
        self.currency = currency

    def pre_json_dict(self):
        """转换为支持 json.dumps 的字典"""
        return {
            'name': self.name,
            'symbol': self.symbol,
            'time': self.time.strftime(self.DATE_FORMAT),
            'open': float(self.open),
            'high': float(self.high),
            'low': float(self.low),
            'close': float(self.close),
            'volume': float(self.volume),
            'market_cap': float(self.market_cap),
            'currency': self.currency,
        }

    def __str__(self):
        return str(self.pre_json_dict())

    def __repr__(self):
        return str(self.pre_json_dict())


class AbstractDataSource:

    def coin_ids(self) -> List[str]:
        """返回支持的加密货币 ID 列表"""
        raise NotImplementedError

    def historical_data(self, coin_id: str, start_day: datetime.datetime, end_day: datetime.datetime) -> List[Coin]:
        """返回 coin_id 对应的 coin 在 [start_day, end_day] 的数据"""
        raise NotImplementedError
