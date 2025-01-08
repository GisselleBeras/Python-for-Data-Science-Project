#Peer-Graded Assignment
#Analyzing Historical Stock/Revenue Data and Building a Dashboard

!pip install yfinance
!pip install bs4
!pip install nbformat

import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .1)
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


#Question 1: Use yfinance to Extract Stock Data
#Reset the index, save, and display the first five rows of the tesla_data dataframe using the head function. Upload the screenshot of the results.

  tesla = yf.Ticker("TSLA")
  tesla_data = tesla.history(period="max")
  tesla_data.reset_index(inplace=True)
  tesla_data.head()

#Question 2: Use Webscraping to Extract Tesla Revenue Data
#Display the last five rows of the tesla_revenue dataframe using the tail function. Upload a screenshot of the results. Make sure you are using the data from the table named Tesla Quarterly Revenue on the website.

  url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
  html_data = requests.get(url).text
  print(html_data)
  soup = BeautifulSoup(html_data,"html.parser")
  tesla_revenue = pd.DataFrame(columns=["Date","Revenue"])
  read_html_pandas_data = pd.read_html(url)
  read_html_pandas_data[1] #quaterly revenue
  for row in soup.find_all("tbody")[1].find_all('tr'):
      col = row.find_all("td")
      date = col[0].text
      revenue = col[1].text
      tesla_revenue = pd.concat([tesla_revenue,pd.DataFrame({"Date":[date], "Revenue":[revenue]})], ignore_index=True)
  tesla_revenue
  
  tesla_revenue["Revenue"] = tesla_revenue["Revenue"].str.replace(",","")
  tesla_revenue["Revenue"] = tesla_revenue["Revenue"].str.replace("$","")
  tesla_revenue
  tesla_revenue.dropna(inplace=True)
  tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
  
  tesla_revenue.tail()

#Question 3: Use yfinance to Extract Stock Data
#Reset the index, save, and display the first five rows of the gme_data dataframe using the head function. Upload a screenshot of the results.

  gamestop = yf.Ticker("GME")
  gme_data =gamestop.history(period="max")
  gme_data.reset_index(inplace=True)
  gme_data.head()

#Question 4: Use Webscraping to Extract GME Revenue Data
#Display the last five rows of the gme_revenue dataframe using the tail function. Upload a screenshot of the results. Make sure you are using the data from the table named GameStop Quarterly Revenue on the website.

  url_2 = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
  html_data_2 = requests.get(url_2).text
  print(html_data_2)
  soup_2 = BeautifulSoup(html_data_2,"html.parser")
  gme_revenue = pd.DataFrame(columns=["Date","Revenue"])
  read_html_pandas_data_2 = pd.read_html(url_2)
  read_html_pandas_data_2[1] #quaterly revenue
  for row in soup_2.find_all("tbody")[1].find_all('tr'):
      col = row.find_all("td")
      date = col[0].text
      revenue = col[1].text
      gme_revenue = pd.concat([gme_revenue,pd.DataFrame({"Date":[date], "Revenue":[revenue]})], ignore_index=True)
  
  gme_revenue["Revenue"] = gme_revenue["Revenue"].str.replace(",","")
  gme_revenue["Revenue"] = gme_revenue["Revenue"].str.replace("$","")
  gme_revenue.dropna(inplace=True)
  gme_revenue = gme_revenue[gme_revenue["Revenue"] != ""]
  gme_revenue
  
  gme_revenue.tail()

#Question 5: Plot Tesla Stock Graph
#Use the make_graph function to graph the Tesla Stock Data, also provide a title for the graph. Upload a screenshot of your results.

  make_graph(tesla_data, tesla_revenue, 'Tesla')

#Question 6: Plot GameStop Stock Graph
#Use the make_graph function to graph the GameStop Stock Data, also provide a title for the graph. Upload a screenshot of your results.

  make_graph(gme_data, gme_revenue, 'GameStop')
