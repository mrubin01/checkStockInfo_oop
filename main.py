import math

import yfinance as yf
import sys
from datetime import datetime
import warnings
import pandas as pd
import time
import Asset
import csv
warnings.simplefilter("ignore")

START_DATE = datetime(2025, 1, 1)  # YYYY, M, D
END_DATE = datetime(2024, 3, 1)
CURRENT_YEAR = 2025
PREVIOUS_YEAR = 2024

ticker = ["FF"]


def main():
    for t in ticker:
        # create an instance of Equity
        stock = Asset.Equity(t, "NYSE")
        data = stock.get_info()

        if len(data) > 0:
            try:
                name = data["shortName"]
            except:
                name = "N/A"
            try:
                sector = data["sector"]
            except:
                sector = "N/A"
            try:
                country = data["country"]
            except:
                country = "N/A"
            try:
                beta = data["beta"]
            except:
                beta = "N/A"

            print(name, sector, country, beta)

            try:
                price = str(round(data["currentPrice"], 2))
            except:
                price = "N/A"
            try:
                bookValue = str(round(data["bookValue"], 2))
            except:
                bookValue = "N/A"
            try:
                trailingpe = str(round(data["trailingPE"], 2))
            except:
                trailingpe = "N/A"
            try:
                forwardpe = str(round(data["forwardPE"], 2))
            except:
                forwardpe = "N/A"
            try:
                peg = str(round(data["pegRatio"], 2))
            except:
                peg = "N/A"
            try:
                payout = str(round(data["payoutRatio"], 3))
            except:
                payout = "N/A"
            try:
                div_cover = 1 / data["payoutRatio"]
                div_cover = str(round(div_cover, 3))
            except:
                div_cover = "N/A"
            try:
                eps = str(data.info["trailingEps"])
            except:
                eps = "N/A"

            print(price, bookValue, trailingpe, forwardpe, peg, payout, div_cover, eps)

            ytd_dividends = stock.get_ytd_dividend(2025, 3, 1)
            div_2023 = stock.get_yearly_dividend(2023)[0]
            div_2024 = stock.get_yearly_dividend(2024)[0]

            issues_2023 = stock.get_yearly_dividend(2023)[1]
            issues_2024 = stock.get_yearly_dividend(2024)[1]

            print(t, ytd_dividends, div_2023, div_2024)
            print(f"Issues in 2023: {issues_2023}; Issues in 2024: {issues_2024}")
            print(f"{t} ", str(beta), str(ytd_dividends), str(div_2024), str(div_2023))
            print("------------------------\n")

        # this is used to avoid overpassing the request limit per minute
        time.sleep(1)


if __name__ == '__main__':
    main()


