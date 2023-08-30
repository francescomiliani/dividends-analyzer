import requests
import csv

url = "https://www.six-group.com/fqs/ref.json?select=ShortName,ValorId&where=ValorSymbol@SSIRT&orderby=ShortName&pagesize=300&page={}"
filename = "companies.csv"

page = 1
all_companies = []

while True:
    response = requests.get(url.format(page))
    data = response.json()

    if "rowData" in data:
        companies = data["rowData"]
        if len(companies) == 0:
            break
        all_companies.extend(companies)
        page += 1
    else:
        print("No data found in the response.")
        break

with open(filename, "w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    
    # Write header
    csv_writer.writerow(["Company", "Ticker"])
    
    # Write data rows
    for company in all_companies:
        yf_ticker = company[1].replace('CHF4', '')
        csv_writer.writerow([company[0], yf_ticker])

print("Data saved to " + filename)
