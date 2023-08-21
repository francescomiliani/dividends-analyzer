import yfinance as yf
import json
from datetime import datetime, timedelta
import math
import csv

'''
#company = yf.Ticker("TSLA")
company = yf.Ticker("ISP.MI")
company = yf.Ticker("ATH.MI")
#company = yf.Ticker("ENEL.MI")
#series = company.actions.Dividends
#print(json.dumps(company.info, sort_keys=True, indent=4))
#print(company.actions.Dividends)
print(f'currentPrice: {company.info["currentPrice"]}')
print(f'dividendRate: {company.info["dividendRate"]}')
print(f'dividendYield: {company.info["dividendYield"]}')
print(f'lastDividendValue: {company.info["lastDividendValue"]}')
print(f'lastDividendDate: {company.info["lastDividendDate"]}')
'''

def compute_dividend_yield_info(company):
    # STEP 1 - Get dividends series data
    series = company.actions.Dividends
    # print(series)

    # STEP 2 - Compute last dividend value in cumulative way

    last_dividend_date = datetime.strftime(series.index[-1], "%Y-%m-%d")
    last_dividend_value = 0
    current_year = 0
    previous_year = current_year
    init = True
    # Loop in reverse order
    for i, v in series.iloc[::-1].items():
        # print(f'i:{i} - v: {v}')
        current_year = i.year
        if init:
            previous_year = current_year
            init = False
        if current_year == previous_year:
            last_dividend_value += v
        else:
            break
        previous_year = current_year
    # print(f'last_dividend_value: {last_dividend_value}')

    # STEP 3 - Get historical data of stock price
    # Subtract 5 days to be sure to get
    start_date = datetime.strftime(datetime.strptime(last_dividend_date, "%Y-%m-%d") - timedelta(days=5), "%Y-%m-%d")
    end_date = last_dividend_date
    # get historical market data
    hist = company.history(start=start_date, end=end_date, interval="1d")
    # print(hist.Close)
    # Loop the array in reverse order
    for i, v in hist.Close.iloc[::-1].items():
        if not math.isnan(float(v)):
            last_price_with_dividend = v
            break
    #print(f'last_price_with_dividend: {last_price_with_dividend}')

    return last_dividend_value, last_price_with_dividend

company_array = []
with open('companies.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            # print(f'Column names are {", ".join(row)}')
            line_count += 1
        # print(f'\tCompany: {row["Company"]} - Ticker: {row["Ticker"]}.')
        company_array.append(row)
        line_count += 1

print('Ticker, lastPriceWithDividend')
for c in company_array:
    ticker = c["Ticker"]
    company = yf.Ticker(ticker)
    last_dividend_value, last_price_with_dividend = compute_dividend_yield_info(company)
    #print(f'Ticker: {ticker}, last_price_with_dividend: {last_price_with_dividend}')
    print(f'{round(last_price_with_dividend, 3)}')

