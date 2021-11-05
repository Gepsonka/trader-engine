import requests
import os
import json
import pandas as pd
import csv

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

    @classmethod
    def get_all_stock_name(self):
        stock_list=[]
        with open('static/500stock.csv') as file:
            csvfile=csv.reader(file)
            next(csvfile) # We do not need the header
            for row in csvfile:
                stock_list.append(row[0])
        return stock_list
        

    def download_stock_data(self):
        """Download data from server"""
        response=requests.get(f'{self.BASE_URL}/stock/{self.stock_name}/chart/{self.period_of_time}?token={self.API_TOKEN}')
        if response.status_code!=200:
            raise ConnectionError('Cannot get the data from the server: '+ str(response.status_code) +', '+self.stock_name)
        else:
            return response.json()

    
    def save_downloaded_data(self,lock=False):
        """Write downloaded data into /static/stocks forder in stock_{stock name}.json format"""
        if lock:
            lock.acquire()
        with open('static/stocks/'+ self.stock_name +'_stock.json','w') as jsonfile:
            try:
                jsonfile.write(json.dumps(self.download_stock_data()))
            except:
                raise IOError('Cannot write stock charts (OS error)')
            finally:
                if lock:
                    lock.release()
                    jsonfile.close()
                else:pass

    def get_data(self):
        '''Get the data we downloaded into the static dir in json format. Sandbox mode is free but not the actual real data. Perfect
        for testing and simulating purposes.'''
        with open('static/stocks/'+ self.stock_name +'_stock.json','r') as jsonfile:
            data=json.loads(jsonfile.read())
            # Do not return inside the block because if the block does not end in execution the file will not be closed.
        return data

    def load_dataframe(self,strategy:str):
        self.dataframe=pd.read_pickle(os.path.join('static/ready_data',strategy,"calculated_"+self.stock_name+'.pkl'))

    def convert_calculated_data_to_json(self,mode:int=0):
        if self.dataframe.empty:
            raise ValueError("Dataframe is empty")
        stock_dict={}
        for index in range(len(self.dataframe.index)):
            stock_dict[self.dataframe.at[index,'Date']]={
                'Close value':self.dataframe.at[index,'Close value'],
                'Signal to buy': self.dataframe.at[index,'Signal to buy']==1,
                'Signal to sell': self.dataframe.at[index,'Signal to sell']==1,

            }
            if mode==0:
                if not pd.isnull(self.dataframe.at[index,'MACD']):
                    stock_dict[self.dataframe.at[index,'Date']]['MACD']=self.dataframe.at[index,'MACD']
                else:
                    stock_dict[self.dataframe.at[index,'Date']]['MACD']=None
                if not pd.isnull(self.dataframe.at[index,'signal']):
                    stock_dict[self.dataframe.at[index,'Date']]['signal']=self.dataframe.at[index,'signal']
                else:
                    stock_dict[self.dataframe.at[index,'Date']]['signal']=None

            elif mode==1:
                if not pd.isnull(self.dataframe.at[index,'SMA30']):
                    stock_dict[self.dataframe.at[index,'Date']]['SMA30']=self.dataframe.at[index,'SMA30']
                else:
                    stock_dict[self.dataframe.at[index,'Date']]['SMA30']=None
                if not pd.isnull(self.dataframe.at[index,'SMA90']):
                    stock_dict[self.dataframe.at[index,'Date']]['SMA90']=self.dataframe.at[index,'SMA90']
                else:
                    stock_dict[self.dataframe.at[index,'Date']]['SMA90']=None
            
        return stock_dict

        

        
