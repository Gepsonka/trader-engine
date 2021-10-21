import json
import time
import requests
from requests import ConnectionError
import threading
import os
from dotenv import load_dotenv, find_dotenv
import pandas as pd
from ..stock_class.stock_class_base import Stock



class SaveDataImplementation:
    """This class in for divide the huge IO load into threads. Python's stl threads are not as efficent as standard low-lever threads
    because of GIL, but it only supposed to divide IO load so it will do the work for us."""
    # disclaimer: If you have a noisy network connection you might run into some requests.exceptions.SSLError exeptions.
    # some sources says it would disappear with Ethernet cable but on WIFI the system is unable to recover some requests.

    """
    Params
    ------

    time_interval: Same time interval as in the stock class
    stock_class_list: initialised Stock() instances organized in a list
    thread_list: Group of implementation of data fetches organized in a list. Each element of this list is a threading.Thread instance
    
    """
    def __init__(self,time_interval) -> None:
        self.time_interval=time_interval
        self.stock_class_list=[]
        self.thread_list=[]

        self.read_csv_top500()
        self.divide_io()
        self.start_threads()
    
    def read_csv_top500(self):
        """Read 500stock.csv file and store it represented as a Stock() instance in a list"""
        stocks=pd.read_csv('static/500stock.csv')
        for index in range(len(stocks.index)):
            self.stock_class_list.append(Stock(stocks.at[index,'Ticker'],self.time_interval))

    def chunks(self,lst, n):
        """Divide stock_class_list innto chunks. Every thread will get a chunk (sublist) of Stock() instances."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]
    def start_io_per_chunk(self,chunk):
        """Starts operations in the chunks"""
        for x in chunk:
            x.download_stock_data()
            x.save_downloaded_data()

    def join_threads(self):
        for thread in self.thread_list:
            thread.join()
    
    def divide_io(self):
        """Organise threads into a list"""
        self.stock_class_list=self.chunks(self.stock_class_list,50)
        for chunk in self.stock_class_list:
            self.thread_list.append(threading.Thread(target=self.start_io_per_chunk,args=(chunk,)))

    def start_threads(self):
        """Responsible for starting threads. Needs time delay between the start of threads, otherwise the requests 
        would return with a plenty of 429 status code error (this way it does only return with a few 429 :D)"""
        for index, thread in enumerate(self.thread_list):
            thread.start()
            time.sleep(1)





    