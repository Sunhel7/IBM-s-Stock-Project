#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install yfinance')
get_ipython().system('pip install bs4')
get_ipython().system('pip install nbformat')
get_ipython().system('pip install matplotlib')


# In[2]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup


# In[3]:


import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)


# In[4]:


import matplotlib.pyplot as plt

def make_graph(stock_data, revenue_data, stock):
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']

    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # Stock price
    axes[0].plot(pd.to_datetime(stock_data_specific.Date), stock_data_specific.Close.astype("float"), label="Share Price", color="blue")
    axes[0].set_ylabel("Price ($US)")
    axes[0].set_title(f"{stock} - Historical Share Price")

    # Revenue
    axes[1].plot(pd.to_datetime(revenue_data_specific.Date), revenue_data_specific.Revenue.astype("float"), label="Revenue", color="green")
    axes[1].set_ylabel("Revenue ($US Millions)")
    axes[1].set_xlabel("Date")
    axes[1].set_title(f"{stock} - Historical Revenue")

    plt.tight_layout()
    plt.show()


# # Use yfinance to Extract Stock Data

# In[5]:


tesla=yf.Ticker("TSLA")


# In[6]:


tesla_data=tesla.history("max")


# In[7]:


tesla_data.reset_index(inplace=True)
tesla_data.head()


# # Use Webscraping to Extract Tesla Revenue Data

# In[8]:


url="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data=requests.get(url).text


# In[9]:


soup=BeautifulSoup(html_data,"html.parser")


# In[10]:


tesla_revenue=pd.DataFrame(columns=["Date","Revenue"])
for table in soup.find_all("table"):
    if "Tesla Quarterly Revenue" in table.get_text():
        for row in table.find("tbody").find_all("tr"):
            col=row.find_all("td")

            if len(col)==2:
                date=col[0].get_text(strip=True)
                revenue=col[1].get_text(strip=True)

                tesla_revenue=pd.concat(
                    [
                        tesla_revenue,
                        pd.DataFrame({
                            "Date": [date],
                            "Revenue": [revenue]
                        })
                    ],
                    ignore_index=True
                )
        break

tesla_revenue.head()


# In[11]:


tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"",regex=True)


# In[12]:


tesla_revenue.dropna(inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]


# In[13]:


tesla_revenue.tail()


# # Use yfinance to Extract Stock Data

# In[15]:


gme=yf.Ticker("GME")


# In[16]:


gme_data=gme.history(period="max")


# In[17]:


gme_data.reset_index(inplace=True)
gme_data.head()


# # Use Webscraping to Extract GME Revenue Data

# In[18]:


url="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data_2=requests.get(url).text


# In[19]:


soup= BeautifulSoup(html_data_2,"html.parser")


# In[20]:


gme_revenue=pd.DataFrame(columns=["Date","Revenue"])
for row in soup.find_all("tbody")[1].find_all("tr"):
    cols=row.find_all("td")
    if len(cols)>=2:
        date=cols[0].text.strip()
        revenue=cols[1].text.strip()
        gme_revenue=pd.concat([gme_revenue,pd.DataFrame([[date, revenue]], columns=["Date", "Revenue"])],
            ignore_index=True
        )

gme_revenue.head()


# In[21]:


gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(',|\$',"",regex=True)
gme_revenue.dropna(inplace=True)
gme_revenue=gme_revenue[gme_revenue["Revenue"]!= " "]


# In[22]:


gme_revenue.tail()


# In[23]:


make_graph(tesla_data, tesla_revenue, 'Tesla')


# In[24]:


make_graph(gme_data, gme_revenue, 'GameStop')


# In[ ]:




