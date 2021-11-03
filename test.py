from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv()) # load env variables stored in .env file

from trade_operations.strategies.MACD import ShortTermMACD
from trade_operations.io_operations.download_data import SaveDataImplementation
from trade_operations.calculate_data.calculate_data_impletmentation import CalculateDataImplementation
from trade_operations.stock_class.stock_class_base import Stock

if __name__=='__main__':
    z=CalculateDataImplementation(0)
    z.implement_data_read()
    