import yfinance as yf
import csv
import math
from datetime import datetime, timedelta
import time
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import os  # Import the os module for folder handling

# Check if the "output" folder exists and create it if not
output_folder = 'output'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
# Check if the "dataset" folder exists and create it if not
output_folder = 'dataset'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def get_dividend_yield_from_html(ticker):
    url = 'https://finance.yahoo.com/quote/' + ticker
    s = HTMLSession()
    response = s.get(url)
    response.html.render()
    soup = BeautifulSoup(response.text, 'html.parser')
    tag = soup.find(attrs={"data-test": "DIVIDEND_AND_YIELD-value"})
    if tag is not None:
        #print(tag.text)
        str = tag.text.split('(')
        if 'N/A' not in str[1]:
            dividend_yield = str[1].replace('%)', '')
        else:
            dividend_yield = None
        return dividend_yield


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


#####################################################################################
#####################################################################################
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
    # print(f'Processed {line_count} lines.')

companies_info_list = []
company_info_fieldnames = ['Company', 'ISIN', 'Ticker', 'Sector', 'currency', 'currentPrice', 'dividendRate', 'dividendYield',
                           'firstDividendDate', 'lastDividendDate', 'lastDividendValue', 'lastPriceWithDividend']
with open('output/companies_info.csv', mode='w', newline='') as csv_file:
    fieldnames = company_info_fieldnames
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

companies_failed = []
for i in range(len(company_array)):
    ticker = company_array[i]["Ticker"]
    start = time.time()
    try:
        company = yf.Ticker(ticker)
        isin = ticker
        ticker = company.info['symbol']

        # STEP 1 - Save series in a file, to speed up the analysis
        series = company.actions.Dividends
        series.to_csv('dataset/' + ticker + '.csv')

        # STEP 2 - Compute the dividend yield info
        # STEP 2 A - Compute last_dividend_value and last_price_with_dividend
        last_dividend_value, last_price_with_dividend = compute_dividend_yield_info(company)

        # STEP 2 B - Compute last_dividend_value and last_price_with_dividend
        dividend_yield = 0
        dividend_yield_html = get_dividend_yield_from_html(ticker)
        print(f'dividendYield API: {company.info["dividendYield"]} - dividend_yield_html: {dividend_yield_html}')
        if "dividendYield" in company.info and company.info["dividendYield"] is not None:
            if round(company.info["dividendYield"]*100, 2) == dividend_yield_html:
                dividend_yield = company.info["dividendYield"]
            else:
                if dividend_yield is not None:
                    dividend_yield = float(dividend_yield_html)/100
        else:
            dividend_yield = 0
        print(f'Company: {ticker} - dividendYield: {dividend_yield}')

        # STEP 2 D - Collect company info
        company_info = {
            "Company": company.info["longName"] if "longName" not in company.info else company_array[i]["Company"],
            "ISIN": company_array[i]['Ticker'],
            "Ticker": company.info["symbol"],
            "Sector": company.info["sector"] if "sector" not in company.info else company_array[i]["Sector"],
            "currency": company.info["currency"],
            "currentPrice": company.info["currentPrice"],
            "dividendRate": company.info["dividendRate"] if ("dividendRate" in company.info and company.info["dividendRate"] is not None) else 0,
            "dividendYield": dividend_yield,
            "firstDividendDate": datetime.strftime(series.index[0], "%Y-%m-%d"),
            "lastDividendDate": datetime.strftime(series.index[-1], "%Y-%m-%d"),
            "lastDividendValue": last_dividend_value,
            "lastPriceWithDividend": round(last_price_with_dividend, 3)
        }

        # STEP 3 - Append the current downloaded company info into a common file
        with open('output/companies_info.csv', mode='a', encoding='UTF8', newline='') as csv_file:
            fieldnames = company_info_fieldnames
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow(company_info)
        end = time.time()
        print(f'{i + 1}/{len(company_array)} Company: {ticker} downloaded successfully in {(end-start):.2f} seconds !')
    except Exception as e:
        print(f'Exception during {ticker} downloading: {e}')
        companies_failed.append(ticker)

print(f'Errors: {len(companies_failed)} / {len(company_array)}')
print('companies_info.csv has been written successfully!')
