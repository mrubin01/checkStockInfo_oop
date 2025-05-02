import sys
from datetime import datetime
import warnings
import pandas as pd
import time
import Asset
import csv
import peRatioByIndustry
import roeByIndustry
import lists
warnings.simplefilter("ignore")
import yfinance as yf

START_DATE = datetime(2025, 1, 1)  # YYYY, M, D
END_DATE = datetime(2026, 3, 1)
CURRENT_YEAR = 2025
PREVIOUS_YEAR = 2024

industry_pe = peRatioByIndustry.industry_avg_pe
industry_roe = roeByIndustry.industry_avg_roe

ticker = lists.alpaca_tickers


def main():
    print("ticker", "exchange", "name", "sector", "industry", "country", "beta", "price", "PBRatio",
          "DivYieldYTD", "DivYield2024", "Issues2024", "DivYield2023", "Issues2023",
          "payout", "DivCover", "PERatio", "PEvsIndustry", "PEGRatio", "ROE", "ROEvsIndustry")

    for t in ticker:
        # create an instance of Equity
        stock = Asset.Equity(t)
        data = stock.get_info()

        if len(data) > 0:
            try:
                exchange = data["fullExchangeName"]
                print(exchange)
                if exchange.startswith("NYSE"):
                    exchange = "NYSE"
                elif exchange.startswith("NASDAQ") or exchange.startswith("Nasdaq"):
                    exchange = "NASDAQ"
                else:
                    exchange = "N/A"
            except:
                exchange = "N/A"
            stock.exchange = exchange
            try:
                name = data["shortName"]
            except:
                name = "N/A"
            try:
                sector = data["sector"]
            except:
                sector = "N/A"
            try:
                industry = data["industry"]
            except:
                industry = "N/A"
            try:
                country = data["country"]
            except:
                country = "N/A"
            try:
                beta = data["beta"]
            except:
                beta = "N/A"

            try:
                price = str(round(data["currentPrice"], 2))
            except:
                price = "N/A"

            try:
                bookValue = round(data["bookValue"], 2)
            except:
                bookValue = "N/A"
            if bookValue != "N/A":
                pb_ratio = str(round(float(price) / float(bookValue), 3))
            else:
                pb_ratio = "N/A"

            try:
                trailingpe = str(round(data["trailingPE"], 2))
            except:
                trailingpe = "N/A"
            # PE must be lower than the industry average to be considered positive
            pe_compared_to_industry = ""
            try:
                if trailingpe != "N/A" and data["trailingPE"] < industry_pe[industry]:
                    pe_compared_to_industry = "lower"
                elif trailingpe != "N/A" and data["trailingPE"] > industry_pe[industry]:
                    pe_compared_to_industry = "higher"
                else:
                    pe_compared_to_industry = "N/A"
            except:
                pe_compared_to_industry = "N/A"


            try:
                roe = str(round(data["returnOnEquity"] * 100, 2))
            except:
                roe = "N/A"
            # a ROE higher than the industry is considered a good sign, anyway if it's higher than 10/12% it's considered good
            roe_compared_to_industry = ""
            try:
                if roe != "N/A" and data["returnOnEquity"] * 100 < industry_roe[industry]:
                    roe_compared_to_industry = "lower"
                elif roe != "N/A" and data["returnOnEquity"] * 100 > industry_roe[industry]:
                    roe_compared_to_industry = "higher"
                else:
                    roe_compared_to_industry = "N/A"
            except:
                roe_compared_to_industry = "N/A"

            try:
                forwardpe = str(round(data["forwardPE"], 2))
            except:
                forwardpe = "N/A"
            try:
                peg = str(round(data["pegRatio"], 2))
            except:
                peg = "N/A"
            try:
                payout = str(round(data["payoutRatio"] * 100, 3))
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

            ytd_dividends = stock.get_ytd_dividend(2025, 4, 20)
            div_2023 = stock.get_yearly_dividend(2023)[0]
            div_2024 = stock.get_yearly_dividend(2024)[0]

            issues_2023 = stock.get_yearly_dividend(2023)[1]
            issues_2024 = stock.get_yearly_dividend(2024)[1]

            if price != "N/A":
                div_yield_2023 = round((float(div_2023) / float(price)) * 100, 2)
                div_yield_2024 = round((float(div_2024) / float(price)) * 100, 2)
                div_yield_ytd = round((float(ytd_dividends) / float(price)) * 100, 2)
            else:
                div_yield_2023 = "No price"
                div_yield_2024 = "No price"
                div_yield_ytd = "No price"

            # print(t, div_yield_2023, div_yield_2024, div_yield_ytd)
            # print(f"Issues in 2023: {issues_2023}; Issues in 2024: {issues_2024}")
            # print(f"{t} ", str(beta), str(ytd_dividends), str(div_2024), str(div_2023))

            print()

            print(t, "|", exchange, "|", name, "|", sector, "|", industry, "|", country, "|", beta, "|", price, "|", pb_ratio, "|",
                  div_yield_ytd, "|",  div_yield_2024, "|", issues_2024, "|", div_yield_2023, "|", issues_2023, "|",
                  payout, "%", "|", div_cover, "|", trailingpe, "|", pe_compared_to_industry, "|", peg, "|", roe, "|", roe_compared_to_industry)

        # this is used to avoid overpassing the request limit per minute
        time.sleep(1)


if __name__ == '__main__':
    main()


