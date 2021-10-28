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
        with open('static/stocks/'+ self.stock_name +'_stock.json','w') as jsonfile:
            try:
                jsonfile.write(json.dumps(self.download_stock_data()))
            except:
                raise IOError('Cannot write stock charts (OS error)')
            finally:
                lock.release()
                jsonfile.close()

    def get_data(self):
        '''Get the data we downloaded into the static dir in json format. Sandbox mode is free but not the actual real data. Perfect
        for testing and simulating purposes.'''
        with open('static/stocks/'+ self.stock_name +'_stock.json','r') as jsonfile:
            data=json.loads(jsonfile.read())
            # Do not return inside the block because if the block does not end in execution the file will not be closed.
        return data

    def load_dataframe(self):
        self.dataframe=pd.read_pickle('static/ready_data/'+ self.period_of_time +'/calculated_'+self.stock_name+'.pkl')
