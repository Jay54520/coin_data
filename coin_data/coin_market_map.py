# -*- coding: utf-8 -*-

import datetime
import decimal
import json
import requests
from bs4 import BeautifulSoup
from typing import List, Dict

from coin_data.base import AbstractDataSource, Coin


class CoinMarketCap(AbstractDataSource):
    QUERY_TIME_FORMAT = '%Y%m%d'

    @classmethod
    def coin_ids(self) -> List[str]:
        coin_ids = []
        response = requests.get('https://api.coinmarketcap.com/v2/listings/')
        coins = json.loads(response.content)
        for coin_dict in coins['data']:
            coin_ids.append(coin_dict['website_slug'])
        return coin_ids

    @classmethod
    def historical_data(cls, coin_id: str, start_day: datetime.datetime, end_day: datetime.datetime) -> List[Coin]:
        historical_data = cls._scrape_historical_data(coin_id, start_day, end_day)
        return historical_data

    @classmethod
    def _scrape_historical_data(cls, name: str, start_day: datetime.datetime, end_day: datetime.datetime) -> List[Coin]:
        """抓取 name 在 [start_day, end_day] 的数据"""
        name = name.title()
        historical_data = []
        symbol = cls._get_symbol(name)
        url = 'https://coinmarketcap.com/currencies/{name}/historical-data/?start={start_day}&end={end_day}'.format(
            name=name.lower(),
            start_day=start_day.strftime(cls.QUERY_TIME_FORMAT),
            end_day=end_day.strftime(cls.QUERY_TIME_FORMAT),
        )
        response = requests.get(url)
        partial_data_list = cls._parse_response(response)
        for partial_data in partial_data_list:
            historical_data.append(Coin(
                name=name,
                symbol=symbol,
                **partial_data
            ))
        return historical_data

    @classmethod
    def get_currency_from_symbol(cls, symbol):
        return symbol[3:]

    @classmethod
    def _parse_response(cls, response) -> List[Dict]:
        result = []
        soup = BeautifulSoup(response.text, "html.parser")
        id_historical_data = soup.find(id="historical-data")
        tag_tbody = id_historical_data.find('tbody')
        for tag_tr in tag_tbody.find_all('tr'):
            row = [tag_td.text for tag_td in tag_tr.find_all('td')]
            if 'No data' in row[0]:
                return result
            partial_data = cls._parse_row(row)
            result.append(partial_data)
        return result

    @classmethod
    def _parse_row(cls, row: List[str]) -> Dict:
        """
        :param row: 比如 ['Jan 03, 2018', '886.00', '974.47', '868.45', '962.72', '5,093,160,000', '85,703,500,000']
        """
        return dict(
            time=datetime.datetime.strptime(row[0], '%b %d, %Y'),
            open=cls._clean_num(row[1]),
            high=cls._clean_num(row[2]),
            low=cls._clean_num(row[3]),
            close=cls._clean_num(row[4]),
            volume=cls._clean_num(row[5]),
            market_cap=cls._clean_num(row[6]),
        )

    @classmethod
    def _get_symbol(cls, name: str) -> str:
        """暂时与 name 相同"""
        return name

    @classmethod
    def _clean_num(cls, num_str: str) -> decimal.Decimal:
        # 猜测表示数据不存在，比如 https://coinmarketcap.com/currencies/elacoin/historical-data/?start=20180101&end=20180103
        if num_str == '-':
            return decimal.Decimal(-1)
        return decimal.Decimal(num_str.replace(',', ''))


if __name__ == '__main__':
    print(CoinMarketCap._scrape_historical_data('grandcoin', datetime.datetime(2018, 1, 1), datetime.datetime(2018, 1, 3)))
    print(CoinMarketCap.coin_ids())
