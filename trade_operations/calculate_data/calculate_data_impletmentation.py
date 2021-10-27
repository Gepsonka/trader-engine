import multiprocessing as mp
from multiprocessing import process
import os
import mmap
from trade_operations.strategies.MACD import ShortTermMACD
from itertools import product

MACD_MODE=0
MEAN_REVERSION_MODE=1


class ReadInstances:
    def __init__(self,mode=0) -> None:
        self.mode=mode
        self.stock_name_chunks=self.chunks(list(self.get_stock_names()),mp.cpu_count())
        
        self.manager=mp.Manager()
        self.shared_list=self.manager.list()
        self.process_pool=mp.Pool(processes=mp.cpu_count())
        
    def chunks(self,lst, n):
        """Divide get_otained_stock_names into chunks."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]
    

    def get_stock_names(self):
        path=os.path.join(os.getcwd(),'static/stocks')
        for filename in os.listdir(path):
            yield filename.split('_')[0]

    def read_data(self,chunk,shared_list):
        for x in chunk:
            if self.mode==0:
                yield shared_list.append(ShortTermMACD(x))
            elif self.mode==1:
                raise NotImplementedError("Only MACD strategy implemented yet!")
                exit(-1)
    def map_operations_to_processes(self):
        ready_data=self.process_pool.starmap(self.read_data,zip(self.chunks,self.shared_list))
        return ready_data
        
class CalculateDataImplementation(ReadInstances):
    def __init__(self,mode) -> None:
        super().__init__(mode)
        
    
    



    




    