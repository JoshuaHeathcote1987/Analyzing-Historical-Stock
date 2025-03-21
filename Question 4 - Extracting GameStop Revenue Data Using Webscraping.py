import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_tesla_revenue():
    url = "https://finance.yahoo.com/quote/GME/financials"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to retrieve data")
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find the financial data table
    table = soup.find('div', class_='table')

    if not table:
        print("Failed to find table data.")
        return None
    
    revenue_data = []
    rows = table.find_all('div', {'class': 'row'})
    
    table_rows = table.find_all(class_="row")  # Find all rows with class "row"

    for row in table_rows:
        columns = row.find_all(class_="column")
        column_texts = [col.text.strip() for col in columns]

        if column_texts and column_texts[0] in ["Total Revenue", "Cost of Revenue"]:
            print(column_texts)


if __name__ == "__main__":
    revenue_df = get_tesla_revenue()
#     if revenue_df is not None:
#         revenue_df.to_csv("tesla_revenue.csv", index=False)
#         print("Tesla revenue data saved to tesla_revenue.csv")