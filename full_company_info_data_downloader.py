import yfinance as yf
import csv
import time

company_array = []
with open('companies.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        company_array.append(row)
        line_count += 1

companies_failed = []
init = True
for i in range(len(company_array)):
    ticker = company_array[i]["Ticker"]
    start = time.time()
    try:
        company = yf.Ticker(ticker)
        if init:
            init = False
            with open('output/companies_full_info.csv', mode='w', newline='') as csv_file:
                fieldnames = company.info.keys()
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
        # STEP 3 - Append the current downloaded company info into a common file
        with open('output/companies_full_info.csv', mode='a', encoding='UTF8', newline='') as csv_file:
            fieldnames = company.info.keys()
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow(company.info)
        end = time.time()
        print(f'{i + 1}/{len(company_array)} Company: {ticker} downloaded successfully in {(end-start):.2f} seconds !')
    except Exception as e:
        print(f'Exception during {ticker} downloading: {e}')
        companies_failed.append(ticker)

print(f'Errors: {len(companies_failed)} / {len(company_array)}')
print('companies_full_info.csv has been written successfully!')
