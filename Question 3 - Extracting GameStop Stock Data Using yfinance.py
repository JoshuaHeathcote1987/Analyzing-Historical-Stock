import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

shopify = yf.Ticker("GME")

shopify_data = shopify.history(period="max")

shopify_data.reset_index(inplace=True)
print(shopify_data.head())
