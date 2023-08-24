import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.milanofinanza.it/quotazioni/ricerca/aggregazione-238-mf-italy-azioni-ordinarie"
filename = "companies.csv"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table")

    if table:
        rows = table.find_all("tr")
        data = []

        for row in rows[1:]:  # Skipping the header row
            cells = row.find_all("td")
            if len(cells) >= 4:  # Assuming there are at least 4 columns in each row
                company_name = cells[0].text.strip()
                codice_isin = cells[len(cells) -1].text.strip()
                data.append([company_name, codice_isin])

        # Save data to CSV file
        with open(filename, "w", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Company", "Ticker"])  # Write header
            csvwriter.writerows(data)  # Write data rows

        print("Data saved to companies.csv")
    else:
        print("Table not found on the page.")
else:
    print("Failed to retrieve the page.")