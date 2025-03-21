import requests
import pandas as pd
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()
    from IPython.display import display, HTML
    fig_html = fig.to_html()
    display(HTML(fig_html))

# Step 1: Download the webpage using requests
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
response = requests.get(url)
html_data_2 = response.text

# Step 2: Parse the HTML data using BeautifulSoup
soup = BeautifulSoup(html_data_2, 'html.parser')

# Step 3: Find the table containing the GameStop revenue data
tables = soup.find_all('table')  # Find all tables on the webpage
gme_revenue_table = None

# Step 4: Loop through the tables to find the "GameStop Revenue" table
for table in tables:
    if "GameStop Revenue" in table.text:
        gme_revenue_table = table
        break  # Exit loop once we find the table

# Step 5: Extract the rows from the table
rows = gme_revenue_table.find_all('tr')[1:]  # Skip the header row

# Step 6: Create an empty DataFrame to store the extracted data
gme_revenue = pd.DataFrame(columns=['Date', 'Revenue'])

# Step 7: Iterate through each row and extract the date and revenue
for row in rows:
    cols = row.find_all('td')
    if len(cols) == 2:  # Ensure there are 2 columns: Date and Revenue
        date = cols[0].text.strip()
        revenue = cols[1].text.strip()

        # Append the extracted data to the DataFrame
        gme_revenue = pd.concat([gme_revenue, pd.DataFrame({'Date': [date], 'Revenue': [revenue]})], ignore_index=True)

# Step 8: Clean the Revenue column by removing commas and dollar signs
gme_revenue['Revenue'] = gme_revenue['Revenue'].str.replace(r',|\$', '', regex=True)

#
print(gme_revenue)