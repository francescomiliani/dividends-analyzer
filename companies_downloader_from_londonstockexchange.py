from bs4 import BeautifulSoup
import pandas as pd
from requests_html import AsyncHTMLSession
asession = AsyncHTMLSession()

base_url = "https://www.londonstockexchange.com/indices/ftse-all-share/constituents/table?page={}"
filename = "companies.csv"
#filename = "companies_from_londonstockexchange.csv"

async def scrape_page(url):
    print("Retrieving " + url)
    r = await asession.get(url)
    await r.html.arender(sleep=3, timeout=60)
    resp=r.html.raw_html
    # print(resp)
    if r.status_code == 200:
        soup = BeautifulSoup(resp, "html.parser")
        table = soup.find("table")

        if table:
            rows = table.find_all("tr")

            data = []
            for row in rows[1:]:  # Skipping the header row
                cells = row.find_all("td")
                if len(cells) >= 2:  # Assuming there are at least 4 columns in each row
                    ticker = cells[0].text.strip()
                    company = cells[1].text.strip()

                    ticker += ".L"  # Adding .L to the ticker to make it compatible with Yahoo Finance
                    data.append([company, ticker])
                    print(f'company {company}, ticker {ticker}')
            return data
        else:
            print("Table not found on the page.")
    else:
        print("Failed to retrieve the page.")

async def main():
    all_data = []
    page = 1
    while True:
        url = base_url.format(page)
        page_data = await scrape_page(url)
        if len(page_data) == 0:  # If the page is empty, we can exit the loop
            break
        all_data += page_data # Otherwise, add the data to the list
        page += 1

    if all_data:
        df = pd.DataFrame(all_data, columns=['Company', 'Ticker'])
        # Remove duplicates
        df.drop_duplicates(inplace=True)
        print(df)
        df.to_csv( filename, index=False)

        print(df)
        print("Data saved to " + filename)
    else:
        print("No data found.")

# Run the main function
asession.run(main)
