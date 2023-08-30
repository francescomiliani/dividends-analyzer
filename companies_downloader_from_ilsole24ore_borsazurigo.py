
import requests
from lxml import html
import re
import csv

base_url = "https://mercati.ilsole24ore.com/azioni/borse-europee/zurigo/{}"
filename = 'companies.csv'

def extract_ticker(href):
    ticker_match = re.search(r"/dettaglio/([A-Z0-9]+\.[A-Z0-9]+)", href)
    return ticker_match.group(1) if ticker_match else None

all_data = []

page = 'A'

while page <= 'Z':
    url = base_url.format(page)
    response = requests.get(url)
    print(url)
    if response.status_code == 200:
        tree = html.fromstring(response.content)
        table = tree.xpath("//table")[1]

        rows = table.xpath(".//tr")
        if len(rows) <= 1:
            break

        for row in rows[1:]:
            columns = row.xpath(".//td")
            nome_a = columns[0].find(".//a")

            if nome_a is not None:
                nome = nome_a.text.strip()
                href = nome_a.get("href")
                #print(href)
                ticker = extract_ticker(href)
                #print(f'company {nome}, ticker {ticker}')
                if ticker is not None:
                    ticker = ticker.replace('ZUR', 'SW') # yahoo finance conversione
                if ticker:
                    print(f'company {nome}, ticker {ticker}')
                    data_row = [nome, ticker]
                    all_data.append(data_row)

        #print(page, end=' ')
        page = chr(ord(page) + 1)
    else:
        print(f"Failed to retrieve the page {page}.")
        break

if all_data:

# Sample list of lists
#data_list = [['q', 1], ['e', 2], ['r', 3], ['e', 2]]

# Convert the list of lists to a DataFrame
    df = pd.DataFrame(all_data, columns=['Company', 'Ticker'])
    # Remove duplicates
    df.drop_duplicates(inplace=True)
    print(df)
    df.to_csv( filename, index=False)

    print("Data saved to companies.csv")
else:
    print("No data found.")
