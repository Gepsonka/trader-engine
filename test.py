from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv()) # load env variables stored in .env file

from trade_operations.strategies.MACD import ShortTermMACD
from trade_operations.io_operations.download_data import SaveDataImplementation
from trade_operations.calculate_data.calculate_data_impletmentation import CalculateDataImplementation


if __name__=='__main__':
    #z=CalculateDataImplementation(0)
    #z.implement()
    # y=SaveDataImplementation('5y')
    x=ShortTermMACD('AAPL','5y')
    # x.implement()