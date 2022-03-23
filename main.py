import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, date
from twilio.rest import Client

today = str(date.today())
today_dt = date.today()
yesterday_dt = today_dt - timedelta(days=1)
STOCK = "HD"
COMPANY_NAME = "Home Depot"


STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

load_dotenv("C:/Users/conno/PycharmProjects/.env.txt")

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol" : STOCK,
    "apikey" : os.getenv("Stock_API_Key")
}

news_parameters = {
    "q": STOCK,
    "from":yesterday_dt,
    "sortBy": "publishedAt",
    "apiKey" : os.getenv("News_API_Key"),
    "language" : 'en'
}

def last_bus_day():
    offset = max(1, (today_dt.weekday() + 6) % 7 - 3)
    timedelta_ = timedelta(offset)
    most_recent = today_dt - timedelta_
    return (f'{most_recent}')


def last_bus_day_1():
    offset = max(1, (yesterday_dt.weekday() + 6) % 7 - 3)
    timedelta2 = timedelta(offset)
    most_recent2 = yesterday_dt - timedelta2
    return(f'{most_recent2}')




response_stock = requests.get(STOCK_ENDPOINT, params=stock_parameters)
response_stock.raise_for_status()
stock_data = response_stock.json()
#print(stock_data)

response_news = requests.get(NEWS_ENDPOINT, params=news_parameters)
response_news.raise_for_status()
news_info = response_news.json()

key_list = []
value_list = []

my_dict = {key_list.append(news_info['articles'][num]['title']): value_list.append(news_info['articles'][num]['description']) for num in range(3)}


# print(key_list)


dt1_cls = float((stock_data["Time Series (Daily)"][last_bus_day()]['4. close']))
dt2_cls = float((stock_data["Time Series (Daily)"][last_bus_day_1()]['4. close']))
difference = round((abs(dt1_cls-dt2_cls)/dt2_cls),3)
diff_pct = difference*100


up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

formatted_articles = [f"Ticker - {STOCK}: {up_down}{diff_pct}%\n\nHeadline: {key_list[num]}. \n\nBrief: {value_list[num]} " for num in range(3)]
print(formatted_articles)
client = Client(os.getenv("My_API_ACCT"), os.getenv("My_Auth_Token"))


for article in formatted_articles:
    message = client.messages \
       .create(
        body = article,
        from_="+19495758903",
        to= os.getenv("My_Cell"))







