from strategy_base import Strategy


class LongTermStrategy(Strategy):
    def __init__(self,stock_name,period_of_time):


        super(LongTermStrategy,self).__init__(stock_name,period_of_time)