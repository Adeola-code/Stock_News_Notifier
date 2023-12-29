import requests
import datetime
from twilio.rest import Client
import os
from decouple import config
yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
day_before_yesterday = (datetime.date.today() - datetime.timedelta(days=2)).strftime('%Y-%m-%d')

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"

# Load environment variables from .env
stock_api_key = config('ALPHA_VANTAGE_API_KEY')
account_sid = config('TWILIO_ACCOUNT_SID')
auth_token = config('TWILIO_AUTH_TOKEN')

stock_params={
    "function":"TIME_SERIES_DAILY",
    "symbol":"TSLA",
    "apikey":stock_api_key,
    "outputsize":"compact"
}
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
news_api_key = config('NEWS_API_KEY')

stock_response=requests.get(STOCK_ENDPOINT, params=stock_params)
stock_response.raise_for_status()
stock_data=stock_response.json()



    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
closing_price_yesterday=stock_data["Time Series (Daily)"][yesterday]["4. close"]
closing_price_yesterday=float(closing_price_yesterday)



#TODO 2. - Get the day before yesterday's closing stock price
closing_price_day_before_yesterday=stock_data["Time Series (Daily)"][day_before_yesterday]["4. close"]
closing_price_day_before_yesterday=float(closing_price_day_before_yesterday)

#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference=closing_price_yesterday - closing_price_day_before_yesterday
up_down=None
if difference>0:
    up_down ="🔺"
else:
    up_down="🔻"
#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percentage_difference = round(((closing_price_yesterday - closing_price_day_before_yesterday) / closing_price_day_before_yesterday) * 100)


#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
if abs(percentage_difference)>0.1:

    news_params = {
        "q": "tesla",
        "from": "2023-10-17",
        "sortBy": "publishedAt",
        "apiKey": news_api_key
    }
    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
    news_response=requests.get(NEWS_ENDPOINT,params=news_params)
    news_response.raise_for_status()
    news_data=news_response.json()["articles"]



    #TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    three_articles= news_data[:3]
        ## STEP 3: Use twilio.com/docs/sms/quickstart/python
        #to send a separate message with each article's title and description to your phone number.

    #TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_articles=[f"{STOCK_NAME}: {up_down}{percentage_difference}%\nHeadline {article['title']} \nBrief: {article['description']}" for article in three_articles]
    #TODO 9. - Send each article as a separate message via Twilio.
    client=Client(account_sid,auth_token)
    for article in formatted_articles:
        message=client.messages.create(
            body=article,
            from_="+17049372724",
            to="+2348064561720"
    )


#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

