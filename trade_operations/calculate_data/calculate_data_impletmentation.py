import multiprocessing as mp
import os
from trade_operations.strategies.MACD import ShortTermMACD

MACD_MODE=0
MEAN_REVERSION_MODE=1

class CalculateDataImplementation:
    def __init__(self,mode:int) -> None:
        self.mode=mode
        self.process_pool=mp.Pool(processes=mp.cpu_count())

        if self.mode==0:
            # self.strategy_classes=[ShortTermMACD(x) for x in self.get_obtained_stock_names()] don't work because one fucker does not
            # follow the form of stock names (its form is something like BD.S)
            self.strategy_classes=list(self.strategy_class_gen())
        elif self.mode==1:
            pass

        self.strategy_class_list_chunks=self.chunks(self.strategy_classes,mp.cpu_count())
    
    def strategy_class_gen(self):
        for x in self.get_obtained_stock_names():
            try:
                print("class_gen")
                yield ShortTermMACD(x)
                
            except:
                continue
    
    def get_stockname_from_filename(self,filename:str):
        '''Extracting the stock name from the filename'''
        stock_name=''
        for x in filename:
            if x.isupper():
                stock_name+=x

        return stock_name

    def get_obtained_stock_names(self):
        path=os.path.join(os.getcwd(),'static/stocks')
        for filename in os.listdir(path):
            yield self.get_stockname_from_filename(filename)
    
    def chunks(self,lst, n):
        """Divide get_otained_stock_names into chunks."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    def calc_chunk(self,chunk):
        for item in chunk:
            item.implement()
            
    def implement(self):
        if self.mode==0: # MACD
            # self.process_pool.map(self.calc_chunk,self.strategy_class_list_chunks)
            pass
        elif self.mode==1: # Mean Reversal
            pass




    