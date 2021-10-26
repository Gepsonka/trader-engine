import json
import pandas as pd
import numpy as np
import asyncio
from dotenv import load_dotenv, find_dotenv
import os
import requests
from ..stock_class.stock_class_base import Stock


load_dotenv(find_dotenv()) # load env variables

"""This file stores the base-class of strategies with all the general functionality every strategy needs."""

"""This data will be visualised on the front-end
using vuejs and apexcharts.js with data served by a django backend"""

# vue docs: https://vuejs.org/
# apexcharts docs: https://apexcharts.com/docs/
# django docs: https://docs.djangoproject.com/en/3.2/ 


class Strategy(Stock):
    '''Base class of all the strategies that will be used in this program.'''
    # BASE_URL = 'https://sandbox.iexapis.com/stable'
    # API_TOKEN = os.environ.get('API_TOKEN')
    BASE_COLUMN_NAMES=['Date', 'Close value', 'high', 'low','Signal to buy','Signal to sell']
    SPECIFIC_COLUMN_NAMES=[]
    
    def __init__(self, stock_name, period_of_time='5y'):
        super().__init__(stock_name,period_of_time)
        # self.stock_name = stock_name  # what kind of stock: aapl, msft...
        # self.period_of_time = period_of_time # _y or _m or _mm or _d or max: given in a string
        self.dataframe=self.fill_pandas_dataframe()

    def get_data(self):
        '''Get the data we downloaded into the static dir in json format. Sandbox mode is free but not the actual real data. Perfect
        for testing and simulating purposes.'''
        with open('static/stocks/stock_'+self.stock_name+'.json','r') as jsonfile:
            data=json.loads(jsonfile.read())
            # Do not return inside the block because if the block does not end in execution the file will not be closed.
        
        return data

    def fill_pandas_dataframe(self):
        '''Upload downloaded data into a pandas DataFrame. It will make the data much easier to work with.
        Every strategy requires different columns in the dataframe. We have predefined which are the same at every strategy
        and we have SPECIFIC_COLUMN_NAMES, which colums are different at every strategy.'''
        df = pd.DataFrame(columns=self.BASE_COLUMN_NAMES+self.SPECIFIC_COLUMN_NAMES)
        df_additional_row_data={}
        for name in self.SPECIFIC_COLUMN_NAMES:
            df_additional_row_data[name]=np.NAN # Fill the empty columns with numpy.NANs

        for row in self.get_data():
            df_row = {'Date': row['date'], 'Close value': row['close'],
            'high': row['high'], 'low': row['low'],'Signal to buy': np.NAN, 'Signal to sell': np.NAN}
            df_row={**df_row,**df_additional_row_data} # Merge the two dicts into one (BASE_COLUMN_NAMES + SPECIFIC_COLUMN_NAMES)
            ser = pd.Series(df_row)
            df = df.append(ser, ignore_index=True)
        return df

    def save_dataframe(self,strategy="MACD"):
        """Save ready dataframe in the proper format (pickle). (I try to adapt to the apexchart's required dataformat)"""
        self.dataframe.to_pickle('static/ready_data/'+ strategy +'/calculated_'+ self.stock_name +'.pkl')
    
    def load_dataframe(self):
        self.dataframe=pd.read_pickle('static/ready_data/'+ self.period_of_time +'/calculated_'+self.stock_name+'.pkl')