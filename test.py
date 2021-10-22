from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv()) # load env variables stored in .env file


from trade_operations.strategies.MACD import ShortTermMACD
from trade_operations.io_operations.download_data import SaveDataImplementation


#y=SaveDataImplementation('5y')


x=ShortTermMACD('AAP','5y')