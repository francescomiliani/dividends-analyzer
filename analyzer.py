import csv
from datetime import datetime
import json
import pandas as pd


def analyze(_company):
    # get stock info
    company_info = _company

    first_year = 0
    yield_counter = 0
    longest_yield_strike = 0
    current_yield_strike = 0
    previous_year = None
    init = True

    with open('dataset/' + _company["Ticker"] + '.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            current_year = datetime.strptime(row["Date"], "%Y-%m-%d").year
            # Skip the current year because not all companies have yet detached the dividend in the current year
            if current_year == datetime.now().year:
                break
            if init:
                first_year = current_year
                previous_year = current_year
                current_yield_strike = 0
                init = False

            if (current_year - previous_year) == 1:  # subsequent years
                current_yield_strike += 1
                if current_yield_strike > longest_yield_strike:
                    longest_yield_strike = current_yield_strike
            elif (current_year - previous_year) > 0:  # subsequent years
                current_yield_strike = 0
            if (current_year - previous_year) != 0:  # do not count equal years e.g. 2000 and 2000
                yield_counter += 1
            previous_year = current_year

    year_time_period = (datetime.now().year - 1) - first_year  # Exclude the current year
    longest_yield_strike_ratio_str = (str(longest_yield_strike) + ' / ' + str(year_time_period)) if (
            longest_yield_strike != 0) else 0
    yield_ratio_str = (str(yield_counter) + ' / ' + str(year_time_period)) if (yield_counter != 0) else 0
    dividend_yield = 0
    if company_info["dividendYield"] != 0:
        dividend_yield = float(company_info["dividendYield"]) * 100
    else:
        if float(company_info["lastPriceWithDividend"]) != 0:
            dividend_yield = float(company_info["lastDividendValue"])/float(company_info["lastPriceWithDividend"]) * 100
        # else: dividend_yield = 0 but it's already set to 0

    _company["longestYieldStrike"] = longest_yield_strike
    _company["yieldCounter"] = yield_counter
    _company["yieldRatio"] = yield_counter / year_time_period * 100
    _company["yearTimePeriod"] = year_time_period
    _company["currentPrice"] = float(company_info["currentPrice"])
    _company["currency"] = company_info["currency"]
    _company["dividendYieldAPI"] = float(_company["dividendYield"]) # Save the original dividendYield
    _company["dividendYield"] = round(dividend_yield, 3) # new dividendYield

    print(f'\t\t Yield ratio: {yield_ratio_str} ({_company["yieldRatio"]} %) - '
          f'Longest yield strike: {longest_yield_strike_ratio_str} - '
          f'Current Price: {_company["currentPrice"]} {_company["currency"]} - '
          f'Dividend Yield: {dividend_yield} %'
          )
    return _company


# ==============================================================================
# ==============================================================================

company_array = []
with open('output/companies_info.csv', mode='r') as csv_file:
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

for i in range(len(company_array)):
    print(f'{i + 1}/{len(company_array)} Company analysis: {company_array[i]["Ticker"]}')
    try:
        company_array[i] = analyze(company_array[i])
    except Exception as e:
        print(e)

# yieldRatio and yearTimePeriod in reverse order
# currentPrice in natural order
ordered_list = sorted(company_array, key=lambda d: (d["yieldRatio"], d["yearTimePeriod"], d["dividendYield"],
                                                    -d["currentPrice"]), reverse=True)

with open('output/analysis.csv', mode='w', newline='') as csv_file:
    fieldnames = ['Company', 'Ticker', 'Sector', 'currency', 'currentPrice', 'dividendRate', 'dividendYield',
                  'dividendYieldAPI', 'longestYieldStrike', 'yearTimePeriod', 'yieldCounter', 'yieldRatio',
                  'firstDividendDate', 'lastDividendDate', 'lastDividendValue', 'lastPriceWithDividend']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(ordered_list)

print(f'analysis.csv file has been written successfully!')

print(f'Let\'s show the first 10 companies')
counter = 10
top_companies_ordered_list = ordered_list[0:counter - 1]
for e in top_companies_ordered_list:
    print(json.dumps(e, sort_keys=True, indent=4))

read_file = pd.read_csv('output/analysis.csv')
read_file.to_excel('output/Analysis.xlsx', index=None, header=True)
print(f'analysis.csv converted in .xlsx successfully!')
