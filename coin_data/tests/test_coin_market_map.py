# -*- coding: utf-8 -*-
import time

import datetime
import unittest

from coin_data.coin_market_map import CoinMarketCap


class TestCoinMarketMap(unittest.TestCase):

    def test_main(self):
        """测试能正常获取前 N 个的数据，表示这个数据源没有大问题"""
        N = 20
        coin_ids = CoinMarketCap.coin_ids()[:20]
        for coin_id in coin_ids:
            historical_data = CoinMarketCap.historical_data(coin_id, datetime.datetime(2018, 1, 1), datetime.datetime(2018, 1, 3))
            print(historical_data)
            assert historical_data[0].time == datetime.datetime(2018, 1, 3)
            # 控制请求频率：Please limit requests to no more than 30 per minute.
            time.sleep(2)
