# -*- coding: utf-8 -*-
from coin_data.base import AbstractDataSource
from coin_data.coin_market_map import CoinMarketCap


def make_data_source(*args, **kwargs) -> AbstractDataSource:
    """根据参数返回实例化的 data_source"""
    return CoinMarketCap()
