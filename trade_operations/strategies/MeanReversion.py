from .strategy_base import Strategy
from .MACD import MACD


class MeanReversion(MACD):
    SPECIFIC_COLUMN_NAMES=['SMA30','SMA90']

    def __init__(self, stock_name, period_of_time='5y'):
        super().__init__(stock_name, period_of_time)

        self.stock_name=stock_name

    def calculate_data(self):
        for index in range(len(self.dataframe.index)):
            if index>=30:
                self.dataframe.at[index,'SMA30']=self.calc_SMA(30,index)
            if index>=90:
                self.dataframe.at[index,'SMA90']=self.calc_SMA(90,index)


    def calc_buy_sell_signals(self):
        for index in range(len(self.dataframe.index)):
            if index>90:
                if self.dataframe.at[index-1,'SMA30']<self.dataframe.at[index-1,'SMA90'] and self.dataframe.at[index,'SMA30']>self.dataframe.at[index,'SMA90']:
                    self.dataframe.at[index,'Signal to buy']=0
                    self.dataframe.at[index,'Signal to sell']=1
                elif self.dataframe.at[index-1,'SMA30']>self.dataframe.at[index-1,'SMA90'] and self.dataframe.at[index,'SMA30']<self.dataframe.at[index,'SMA90']:
                    self.dataframe.at[index,'Signal to buy']=1
                    self.dataframe.at[index,'Signal to sell']=0
                elif self.dataframe.at[index-1,'SMA30']==self.dataframe.at[index-1,'SMA90']:
                    self.dataframe.at[index,'Signal to buy']=0
                    self.dataframe.at[index,'Signal to sell']=0
                else:
                    self.dataframe.at[index,'Signal to buy']=0
                    self.dataframe.at[index,'Signal to sell']=0
    def implement(self):
        self.calculate_data()
        self.calc_buy_sell_signals()
        self.save_dataframe(strategy='MeanReversion')





