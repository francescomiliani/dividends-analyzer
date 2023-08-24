import requests
import pandas as pd

base_url = "https://mercati.ilsole24ore.com/azioni/borsa-italiana/ftse-all-share/{}"
filename = "companies_from_ilsole24ore.csv"

def scrape_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        dfs = pd.read_html(response.text)  # Parse HTML tables using pandas
        if dfs:
            df = dfs[0]
            df = df[["Nome", "ISIN", "Categoria"]]  # Extract specific columns            
            return df
        else:
            print("Table not found on the page.")
    else:
        print("Failed to retrieve the page.")

    return pd.DataFrame()

all_data = []
page = 1
while True:
    url = base_url.format(page)
    page_data = scrape_page(url)
    if page_data.empty:
        break
    all_data.append(page_data)
    page += 1

if all_data:
    combined_data = pd.concat(all_data, ignore_index=True)
    combined_data.rename(columns={'Nome': 'Company',
                                  'ISIN': 'Ticker',
                                  'Categoria': 'Sector',
                               }, inplace=True)
    combined_data.to_csv(filename, index=False)

    print(combined_data)
    print("Data saved to " + filename)
else:
    print("No data found.")
