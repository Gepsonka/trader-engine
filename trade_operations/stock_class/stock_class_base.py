import requests
import os
import json


class Stock:
    """Represents a stock
    
    Params
    ------

    stock_name : Name of the stock, loaded from 500stock.csv.
    time_interval : The amount of data we want to fetch from the IEX cloud api from the given stock (5y/2y/2m/...) given as a string.
    
    Class variables
    ---------------

    BASE_URL: Base url of our api. We will concatenate the rest of the URI to this string
    API_TOKEN: Token for the api passed to the URI as an url query (?token=cscsdsdccycy)

    """
    BASE_URL = 'https://sandbox.iexapis.com/stable'
    API_TOKEN = os.environ.get('API_TOKEN')

    def __init__(self,stock_name,period_of_time='5y') -> None:
        self.stock_name=stock_name
        self.period_of_time=period_of_time

    def download_stock_data(self):
        """Download data from server"""
        response=requests.get(f'{self.BASE_URL}/stock/aapl/chart/{self.period_of_time}?token={self.API_TOKEN}')
        if response.status_code!=200:
            raise ConnectionError('Cannot get the data from the server: '+ str(response.status_code) +', '+self.stock_name)
        else:
            return response.json()

    
    def save_downloaded_data(self,lock):
        """Write downloaded data into /static/stocks forder in stock_{stock name}.json format"""
        lock.acquire()
        with open('static/stocks/stock_'+ self.stock_name +'.json','w') as jsonfile:
            try:
                jsonfile.write(json.dumps(self.download_stock_data()))
            except:
                raise IOError('Cannot write stock charts (OS error)')
            finally:
                lock.release()
                jsonfile.close()
