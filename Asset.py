import yfinance as yf
from datetime import datetime
import requests_cache
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# set up a user-agent to avoid error 429 in yfinance (Too many requests): it doesn't fix the error
session = requests_cache.CachedSession('yfinance.cache')
# the user-agent string comes from the developer tool in Firefox
session.headers['User-agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:132.0) Gecko/20100101 Firefox/132.0"
# empty the cache
session.cache.clear()


class Asset(object):
    # constructor
    def __init__(self, symbol: str):
        self.symbol = symbol

    def __str__(self):
        return f"{self.symbol} is an asset"

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, new_symbol: str):
        if isinstance(new_symbol, str):
            self._symbol = new_symbol
        else:
            print("Invalid symbol! It must be a string")


# child class
class Equity(Asset):
    # override constructor
    def __init__(self, symbol, exchange="Unknown"):
        super(Equity, self).__init__(symbol)

        self.exchange = exchange

    def __str__(self):
        return f"{self.symbol} is an equity, its exchange is {self.exchange}"

    @property
    def exchange(self):
        return self._exchange

    @exchange.setter
    def exchange(self, new_exchange: str):
        if isinstance(new_exchange, str):
            self._exchange = new_exchange
        else:
            print("Invalid exchange! It must be a string")

    def get_info(self):
        """ Call Yahoo Finance API and store data into a dict """
        try:
            stock = yf.Ticker(self._symbol, session=session)
            info = stock.info
            return info
        except:
            return {}
    #
    # @classmethod method calling another class method
    # def get_name(cls, method):
    #     name = method["shortName"]
    #     return name

    def get_yearly_dividend(self, year: int) -> list:
        """ Returns the sum of the dividends issued in a specific year
            and how many dividend issues
        :param year: the year in format YYYY
        :return: a list with the sum of dividends YTD and the number of issues
        """
        start = datetime(year, 1, 1)
        end = datetime(year + 1, 1, 1)
        issues_per_year = 0
        try:
            stock = yf.Ticker(self._symbol, session=session)
            div = stock.history(start=start, end=end)["Dividends"].to_frame(name=self.symbol)
            tot_div = round(div.sum()[0], 3)
            # compute the issues per year
            for index, row in div.iterrows():
                if row[0] > 0:
                    issues_per_year += 1
        except:
            return [-999999, -999999]

        return [tot_div, issues_per_year]

    def get_ytd_dividend(self, current_year: int, month: 1, day: 1) -> float:
        """
        :param current_year: the current year YYYY
        :param month: in format M
        :param day: in format D
        :return: the sum of dividends YTD
        """
        start_date = datetime(current_year, 1, 1)
        # if month and day are not provided, it's assumed to be the first day of the following year
        end_date = datetime(current_year + 1, month, day)

        try:
            stock = yf.Ticker(self._symbol, session=session)
            div = stock.history(start=start_date, end=end_date)["Dividends"].to_frame(name=self.symbol)
            ytd_div = round(div.sum()[0], 3)
        except:
            return -999999

        return ytd_div

    def get_all_dividends(self):
        """ List all dividends from inception sorted by date """
        try:
            stock = yf.Ticker(self._symbol, session=session)
            div = stock.dividends.to_frame(name="Div")
        except:
            return -999999

        if len(div) > 0:
            return div
        else:
            return 0



