import json
import pandas as pd
import numpy as np
import asyncio
from dotenv import load_dotenv, find_dotenv
import os
import requests

load_dotenv(find_dotenv())


class Strategy:
    '''Base class of all the strategies that will be used in this program.'''
    BASE_URL = 'https://sandbox.iexapis.com/stable'
    API_TOKEN = os.environ.get('API_TOKEN')
    
    def __init__(self, stock_name, period_of_time):
        self.stock_name = stock_name  # what kind of stock: aapl, msft...
        # _y or _m or _mm or _d or max: given in a string
        self.period_of_time = period_of_time
        

    def get_data(self):
        '''Get the data we downloaded into the static dir in json format. Sandbox mode is free but not the actual real data. Perfect
            for testing and simulating purposes.'''
        with open(f'static/stocks/stock_{self.stock_name}.json') as jsonfile:
            return json.load(jsonfile)

    def ema(self,price_today,k,number_of_days,EMA_yesterday):
        return price_today*k+EMA_yesterday*(1-k)
