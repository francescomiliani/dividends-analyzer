import requests
from lxml import html
import re
import csv
import json

base_url = "https://www.borsaitaliana.it/borsa/azioni/all-share/lista.html?&page={}"
filename = 'companies_from_swissexchange.csv'
def extract_isin(href):
    isin_match = re.search(r"/scheda/(\w+)\.html", href)
    return isin_match.group(1) if isin_match else None

all_data = []

page = 1
while True:
    url = base_url.format(page)
    response = requests.get(url)

    if response.status_code == 200:
        tree = html.fromstring(response.content)
        table = tree.xpath("//table")[1]

        rows = table.xpath(".//tr")
        if len(rows) <= 1:
            break

        for row in rows[1:]:
            columns = row.xpath(".//td")
            nome_a = columns[1].find(".//a")
            if nome_a is not None:
                nome = nome_a.text.strip()
                href = nome_a.get("href")
                isin = extract_isin(href)
                print(nome, isin)

                if isin:
                    data_row = [nome, isin]
                    all_data.append(data_row)

        page += 1
    else:
        print(f"Failed to retrieve the page {page}.")
        break

if all_data:
    with open(filename, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Company", "Ticker"])  # Write header
        csvwriter.writerows(all_data)  # Write data rows
    print("Data saved to companies.csv")
else:
    print("No data found.")
