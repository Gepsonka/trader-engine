# This file is only for testing purposes. Has no representation in the actual code.
from pandas.core.dtypes.missing import isnull
import requests
import pandas as pd
import numpy as np
import json


API_TOKEN='Tpk_059b97af715d417d9f49f50b51b1c448'
BASE_URL='https://sandbox.iexapis.com/stable'


#response=requests.get(f'{BASE_URL}/stable/stock/aapl/chart/1y?token={API_TOKEN}')
# We save the data in a json file
with open('static/res.json') as jsonfile:
    STOCK_EX_CHART=json.load(jsonfile)
    jsonfile.close()

columns=['Date','Close value','high','low','SMA12','EMA12','SMA26','EMA26','MACD','signal','Signal to buy','Signal to sell']



dataframe=pd.DataFrame(columns=columns)
SMOOTHING=2
i=0
for row in STOCK_EX_CHART:
    row = {'Date': row['date'], 'Close value': row['close'],
           'high': row['high'], 'low': row['low'], 'SMA12': np.NAN, 'EMA12': np.NAN,
           'SMA26': np.NAN, 'EMA26': np.NAN,'MACD':np.NAN,'signal':np.NAN, 'Signal to buy': np.NAN, 'Signal to sell': np.NAN}
    ser=pd.Series(row)
    dataframe=dataframe.append(ser,ignore_index=True)
    if i>=12:
        avg_frame12=dataframe.iloc[i-12:i]
        avg12=avg_frame12['Close value'].mean()
        dataframe.at[i,'SMA12']=avg12
    if i>=13:
        if pd.isnull(dataframe.at[i-1,'EMA12']):
            yesterday_EMA12=dataframe.at[i-1,'SMA12']
        else:
            yesterday_EMA12=dataframe.at[i-1,'EMA12']
        k=2/(12+1)
        today_EMA12=dataframe.at[i,'Close value']*k+yesterday_EMA12*(1-k)
        dataframe.at[i,'EMA12']=today_EMA12

    if i>=26:
        avg_frame26=dataframe.iloc[i-26:i]
        avg26=avg_frame26['Close value'].mean()
        dataframe.at[i,'SMA26']=avg26
    if i>=27:
        if pd.isnull(dataframe.at[i-1,'EMA26']):
            yesterday_EMA26=dataframe.at[i-1,'SMA26']
        else:
            yesterday_EMA26=dataframe.at[i-1,'EMA26']

        k=2/(26+1)
        today_EMA26=dataframe.at[i,'Close value']*k+yesterday_EMA26*(1-k)
        dataframe.at[i,'EMA26']=today_EMA26
        
        
    if not pd.isnull(dataframe.at[i,'EMA12']) and not pd.isnull(dataframe.at[i,'EMA26']):
        macd=dataframe.at[i,'EMA12']-dataframe.at[i,'EMA26']
        dataframe.at[i,'MACD']=dataframe.at[i,'EMA12']-dataframe.at[i,'EMA26']
    i+=1



print(dataframe)

