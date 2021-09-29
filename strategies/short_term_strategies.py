from strategy_base import Strategy
import pandas as pd
import numpy as np


class ShortTermStrategy(Strategy):
    def __init__(self,stock_name,period_of_time):
        super(ShortTermStrategy,self).__init__(stock_name,period_of_time)

    def smoothing(self,number_of_days):
        """Smoothing formula used for calculating exponential moving averages (EMA)"""
        return 2/(number_of_days+1)
    
    


class ShortTermMACD(ShortTermStrategy):
    """Parent class ot the MACD strategies."""
    DATAFRAME_COLUMNS = ['Date', 'Close value', 'high', 'low','SMA9', 'SMA12', 'EMA12',
                         'SMA26', 'EMA26', 'MACD', 'signal', 'Signal to buy', 'Signal to sell']

    def __init__(self,stock_name,period_of_time):
        self.chart=self.get_data()
        self.dataframe = self.fill_pandas_dataframe()

        super(ShortTermMACD,self).__init__(stock_name,period_of_time)
    
    def fill_pandas_dataframe(self):
        '''Upload downloaded data into a pandas DataFrame. It will make the data much easier to work with.'''
        df = pd.DataFrame(columns=self.DATAFRAME_COLUMNS)
        for row in self.get_data():
            row = {'Date': row['date'], 'Close value': row['close'],
            'high': row['high'], 'low': row['low'],'SMA9':np.NAN, 'SMA12': np.NAN, 'EMA12': np.NAN,
            'SMA26': np.NAN, 'EMA26': np.NAN, 'MACD': np.NAN, 'signal': np.NAN, 'Signal to buy': np.NAN, 'Signal to sell': np.NAN}
            ser = pd.Series(row)
            df = df.append(ser, ignore_index=True)
        
        return df
    
    def calc_SMA(self,number_of_days,index):
        if index>=number_of_days:
            avg_frame=self.dataframe.iloc[index-number_of_days:index]
            avg=avg_frame['Close value'].mean()
            return avg
        else:
            raise ValueError(f'{number_of_days} days must pass before you can calculate this SMA')
    
    def calc_ema(self,price_today,k,number_of_days,EMA_yesterday,index):
        if index>=number_of_days+1:
                k=self.smoothing(number_of_days)
                today_EMA=self.ema(self.dataframe.at[index,'Close value'],k,number_of_days,EMA_yesterday)
                self.ema(self.dataframe.at[index,'Close value'],k,number_of_days,EMA_yesterday)
                # self.dataframe.at[index,'EMA'+str(number_of_days)]=today_EMA
                return today_EMA
        else:
            raise ValueError(f'{number_of_days} days must pass before you can calculate this EMA')


    
    def calc_SMA12_for_dataframe(self):
        """Calculate 12-day simple moving average (SMA) for each day of the charts"""
        for index in range(len(self.dataframe.index)):
            if index>=12:
                self.dataframe.at[index,]

    def calc_SMA26_for_dataframe(self):
        """Calculate 26-day simple moving average (SMA) for each day of the charts"""
        for index in range(len(self.dataframe.index)):
            if index>=26:
                avg_frame26=self.dataframe.iloc[index-26:index]
                avg26=avg_frame26['Close value'].mean()
                self.dataframe.at[index,'SMA26']=avg26

    def calc_EMA12_for_dataframe(self):
        """Calculate 12-day exponential moving average (EMA) for each day of the charts."""
        for index in range(len(self.dataframe.index)):
            if index>=12+1:
                if pd.isnull(self.dataframe.at[index-1,'EMA12']):
                    yesterday_EMA12=self.dataframe.at[index-1,'SMA12']
                else:
                    yesterday_EMA12=self.dataframe.at[index-1,'EMA12']
                k=self.smoothing(12)
                today_EMA12=self.dataframe.at[index,'Close value']*k+yesterday_EMA12*(1-k)
                self.dataframe.at[index,'EMA12']=today_EMA12

    def calc_EMA26_for_dataframe(self):
        """Calculate 26-day exponential moving average (EMA) for each day of the charts."""
        for index in range(len(self.dataframe.index)):
            if index>=27:
                if pd.isnull(self.dataframe.at[index-1,'EMA26']):
                    yesterday_EMA26=self.dataframe.at[index-1,'SMA26']
                else:
                    yesterday_EMA26=self.dataframe.at[index-1,'EMA26']

                k=self.smoothing(26)
                today_EMA26=self.dataframe.at[index,'Close value']*k+yesterday_EMA26*(1-k)
                self.dataframe.at[index,'EMA26']=today_EMA26
    
    def calc_EMA12_and_SMA12_for_dataframe(self):
        for index in range(len(self.dataframe.index)):
            if index>=12:
                avg_frame12=self.dataframe.iloc[index-12:index]
                avg12=avg_frame12['Close value'].mean()
                self.dataframe.at[index,'SMA12']=avg12
            
            if index>=12+1:
                if pd.isnull(self.dataframe.at[index-1,'EMA12']):
                    yesterday_EMA12=self.dataframe.at[index-1,'SMA12']
                else:
                    yesterday_EMA12=self.dataframe.at[index-1,'EMA12']
                k=self.smoothing(12)
                today_EMA12=self.dataframe.at[index,'Close value']*k+yesterday_EMA12*(1-k)
                self.dataframe.at[index,'EMA12']=today_EMA12

        
        #wrapped up different calculations into one loop due to performace issues, but i left the individual ones if needed
    def calc_EMA26_and_SMA26_for_dataframe(self):
        for index in range(len(self.dataframe.index)):
            if index>=26:
                avg_frame26=self.dataframe.iloc[index-26:index]
                avg26=avg_frame26['Close value'].mean()
                self.dataframe.at[index,'SMA26']=avg26
            if index>=27:
                if pd.isnull(self.dataframe.at[index-1,'EMA26']):
                    yesterday_EMA26=self.dataframe.at[index-1,'SMA26']
                else:
                    yesterday_EMA26=self.dataframe.at[index-1,'EMA26']

                k=self.smoothing(26)
                today_EMA26=self.dataframe.at[index,'Close value']*k+yesterday_EMA26*(1-k)
                self.dataframe.at[index,'EMA26']=today_EMA26

    def calc_EMA26_and_SMA26_and_EMA12_and_SMA12_for_dataframe(self):
        for index in range(len(self.dataframe.index)):
            if index>=9:
                avg_frame9=self.dataframe.iloc[index-9:index]
                avg9=avg_frame9['Close value'].mean()
                self.dataframe.at[index,'SMA9']=avg9
            if index>=12:
                avg_frame12=self.dataframe.iloc[index-12:index]
                avg12=avg_frame12['Close value'].mean()
                self.dataframe.at[index,'SMA12']=avg12
            if index>=26:
                avg_frame26=self.dataframe.iloc[index-26:index]
                avg26=avg_frame26['Close value'].mean()
                self.dataframe.at[index,'SMA26']=avg26
            if index>=9+1:
                if pd.isnull(self.dataframe.at[index-1,'EMA9']):
                    yesterday_EMA9=self.dataframe.at[index-1,'SMA9']
                else:
                    yesterday_EMA9=self.dataframe.at[index-1,'EMA9']
                k=self.smoothing(9)
                today_EMA9=self.dataframe.at[index,'Close value']*k+yesterday_EMA9*(1-k)
                self.dataframe.at[index,'EMA9']=today_EMA9
            if index>=12+1:
                if pd.isnull(self.dataframe.at[index-1,'EMA12']):
                    yesterday_EMA12=self.dataframe.at[index-1,'SMA12']
                else:
                    yesterday_EMA12=self.dataframe.at[index-1,'EMA12']
                k=self.smoothing(12)
                today_EMA12=self.dataframe.at[index,'Close value']*k+yesterday_EMA12*(1-k)
                self.dataframe.at[index,'EMA12']=today_EMA12
            if index>=26+1:
                if pd.isnull(self.dataframe.at[index-1,'EMA26']):
                    yesterday_EMA26=self.dataframe.at[index-1,'SMA26']
                else:
                    yesterday_EMA26=self.dataframe.at[index-1,'EMA26']

                k=self.smoothing(26)
                today_EMA26=self.dataframe.at[index,'Close value']*k+yesterday_EMA26*(1-k)
                self.dataframe.at[index,'EMA26']=today_EMA26
        #wrapped up bc of performance reasons
    def calc_MACD(self):
        number_of_macd_calculated=0
        for index in range(len(self.dataframe.index)):
            if not pd.isnull(self.dataframe.at[index,'EMA12']) and not pd.isnull(self.dataframe.at[index,'EMA26']):
                macd=self.dataframe.at[index,'EMA12']-self.dataframe.at[index,'EMA26']
                self.dataframe.at[index,'MACD']=self.dataframe.at[index,'EMA12']-self.dataframe.at[index,'EMA26']
                number_of_macd_calculated+=1
            if number_of_macd_calculated>=9:
                if pd.isnull(self.dataframe.at[index-1,'EMA9']):
                    yesterday_EMA9=self.dataframe.at[index-1,'SMA9']
                else:
                    yesterday_EMA9=self.dataframe.at[index-1,'EMA9']

                k=self.smoothing(9)
                today_EMA9=self.dataframe.at[index,'Close value']*k+yesterday_EMA9*(1-k)
                self.dataframe.at[index,'EMA9']=today_EMA9


