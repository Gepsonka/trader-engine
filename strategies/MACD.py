from strategy_base import Strategy
import pandas as pd
import numpy as np


"""Moving Average Convergence Divergence strategy is a widely used and essential stock indicator to predict the trend of the stock.
    Its main problem is if the MACD line crosses (or generating a sign to sell or buy) id does not neccesarily mean a trade should be made 
    because sometimes it generates false signs. (When the MACD line crosses but the trend does not change. In this case we lose.)"""

"""Short-term MACD is usually calculated with the 12 and 26-day EMAs, long-term is with 200 and 50 day EMAs."""

"""When the MACD line crosses the signal line (usually the 9-day EMA of the MACD line) from up-to-bottom we sell
if it crosses from the bottom we buy"""

"""Drawback of this strategy is sometimes even when a crossover occurs, the trend does not changes, therefore we lose."""

class MACD(Strategy):
    def __init__(self,stock_name,period_of_time):
        super().__init__(stock_name,period_of_time)

    
    def smoothing(self,number_of_days):
        """Smoothing formula used for calculating exponential moving averages (EMA)"""
        return 2/(number_of_days+1)

    def ema(self,price_today,number_of_days,EMA_yesterday):
        '''Formula of the Exponential Moving Average (EMA)'''
        return price_today*self.smoothing(number_of_days)+EMA_yesterday*(1-self.smoothing(number_of_days))

    def calc_SMA(self,number_of_days,index):
        """Calculate Simple Moving Average (SMA) from the given data (classes dataframe) to the given period of time."""

        if 'SMA'+str(number_of_days) not in self.dataframe.columns:
            raise AttributeError("There is no such column in the datafrmame as SMA"+str(number_of_days))
            #checking if there is such SMA-for-day column in the dataframe, same is implemented in the clac_EMA fuction
        if index>=number_of_days:
            avg_frame=self.dataframe.iloc[index-number_of_days:index]
            avg=avg_frame['Close value'].mean()
            return avg
        else:
            raise ValueError(str(number_of_days)+' days must pass before you can calculate this SMA')
    
    def calc_EMA(self,number_of_days,index):
        """Calculate Exponential Moving Average (EMA) from the given data (classes dataframe) for the given day of the 
        dataframe to the given period of time."""

        if 'EMA'+str(number_of_days) not in self.dataframe.columns:
            raise AttributeError("There is no such column in the datafrmame as EMA"+str(number_of_days))

        if index>=number_of_days+1:
            if pd.isnull(self.dataframe.at[index-1,'EMA'+str(number_of_days)]):
                EMA_yesterday=self.dataframe.at[index-1,'SMA'+str(number_of_days)]
            else:
                EMA_yesterday=self.dataframe.at[index-1,'EMA'+str(number_of_days)]
            today_EMA=self.ema(self.dataframe.at[index,'Close value'],number_of_days,EMA_yesterday)
            #self.ema(self.dataframe.at[index,'Close value'],k,number_of_days,EMA_yesterday)
            # self.dataframe.at[index,'EMA'+str(number_of_days)]=today_EMA
            return today_EMA
        else:
            raise ValueError(str(number_of_days)+' days must pass before you can calculate this EMA')
    
    def calc_MACD(self,index,short_term=True):
        """Calculate the MACD line from The two EMA (12-day EMA - 26-day EMA or 50-day EMA - 200-day EMA)"""
        if 'MACD' not in self.dataframe.columns:
            raise AttributeError("No such column as 'MACD'")
        if short_term:
            starting_index=26+1
        elif not short_term:
            starting_index=200+1      

        if index<starting_index:
            raise ValueError(str(starting_index)+" days must pass before you can calculate the MACD for this day")

        if short_term:
            return self.dataframe.at[index,'EMA12']-self.dataframe.at[index,'EMA26']
        elif not short_term:
            return self.dataframe.at[index,'EMA50']-self.dataframe[index,'EMA200']

    def calc_MACD_SMA(self,index,number_of_days=9,short_term=True):
        """Required to calculate the signal line (usually the 9-day EMA of the MACD line)"""
        if 'MACD_SMA' not in self.dataframe.columns:
            raise AttributeError("There is no such column in the datafrmame as SMA"+str(number_of_days))
            #checking if there is such SMA-for-day column in the dataframe, same is implemented in the clac_EMA fuction
        if short_term:
            if index>=26+number_of_days+1:
                avg_frame=self.dataframe.iloc[index-number_of_days:index]
                avg=avg_frame['MACD'].mean()
                return avg
            else:
                raise ValueError(str(number_of_days)+' days of MACD must be calculated to return the MACD SMA')
        else:
            if index>=200+number_of_days+1:
                avg_frame=self.dataframe.iloc[index-number_of_days:index]
                avg=avg_frame['MACD'].mean()
                return avg
            else:
                raise ValueError(str(number_of_days)+' days of MACD must be calculated to return the MACD SMA')
        

    def calc_signal_line(self,index,short_term=True):
        """9-day or 40-day EMA of the MACD line (or signal line)"""
        if 'signal' not in self.dataframe.columns:
            raise AttributeError("No such columns as 'signal'")

        if self.dataframe.at[index-1,'signal'] is np.NAN:
            if self.dataframe.at[index-1,'MACD_SMA'] is np.NAN:
                raise ValueError("Cannot calculate the signal here! day:"+index-1)
            else:
                EMA_yesterday=self.dataframe.at[index-1,'MACD_SMA']
        else:
            EMA_yesterday=self.dataframe.at[index-1,'signal']

        if short_term:
            return self.ema(self.dataframe.at[index,"MACD"],9,EMA_yesterday)
            
        else:
            return self.ema(self.dataframe.at[index,"MACD"],40,EMA_yesterday)
        




class ShortTermMACD(MACD):
    '''Implementing short-term MACD trading (using 12-day EMA and 26-day EMA)
    
    Params
    ------

    chart: The data returned by the get_data() function
    specific_column_names: Additional pandas dataframe columns which the strategy needs
    
    '''
    SPECIFIC_COLUMN_NAMES=['SMA12','SMA26','EMA12','EMA26','MACD','MACD_SMA','signal']

    def __init__(self,stock_name,period_of_time):
        super().__init__(stock_name,period_of_time)
        self.chart=self.get_data()
        self.stock_name=stock_name

        self.implement()
    
    def calculate_data(self):
        """Fill data with the calculated arguments, with the functions defined in the parent class."""
        
        for index in range(len(self.dataframe.index)):
            if index>=12:
                self.dataframe.at[index,'SMA12']=self.calc_SMA(12, index)

            if index>=26:
                self.dataframe.at[index,'SMA26']=self.calc_SMA(26, index)

            if index>=13:
                self.dataframe.at[index,'EMA12']=self.calc_EMA(12, index)

            if index>=26+1:
                self.dataframe.at[index,'EMA26']=self.calc_EMA(26, index)
                self.dataframe.at[index,'MACD']=self.calc_MACD(index)

            if index>=26+1+9:
                self.dataframe.at[index,'MACD_SMA']=self.calc_MACD_SMA(index)
                
            if index>=26+1+9:
                self.dataframe.at[index,'signal']=self.calc_signal_line(index)
            
        # print('EMAaaa26: '+str(self.dataframe.at[30,'EMA26']))
        print(self.dataframe)

    def implement(self):
        self.calculate_data()


        

                
    