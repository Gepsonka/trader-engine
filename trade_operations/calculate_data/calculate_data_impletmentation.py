import multiprocessing as mp
from multiprocessing import process
from itertools import repeat
import os
import mmap
from trade_operations.stock_class.stock_class_base import Stock
from trade_operations.strategies.MACD import ShortTermMACD
from itertools import product
from functools import partial

MACD_MODE=0
MEAN_REVERSION_MODE=1


class ReadInstances:
    def __init__(self,mode=0) -> None:
        self.mode=mode

        self.stock_name_chunks=list(self.chunks(list(self.get_stock_names()),mp.cpu_count()))
        print(self.stock_name_chunks[0])
        self.manager=mp.Manager()
        self.shared_list=self.manager.list()
        self.process_pool=[mp.Process(target=self.read_data,args=(self.stock_name_chunks[i],)) for i in range(mp.cpu_count())]
        
    def chunks(self,lst, n):
        """Divide lst into n-piece chunks."""
        splited = [lst[i::n] for i in range(n)]
        return splited
    

    def get_stock_names(self):
        path=os.path.join(os.getcwd(),'static/stocks')
        for filename in os.listdir(path):
            yield filename.split('_')[0]

    def read_data(self,chunk):
        for x in chunk:
            if self.mode==0:
                #shared_list.append(ShortTermMACD(x))
                stock_class=ShortTermMACD(x)
                stock_class.implement()
                print("Stock has been processed successfully! "+stock_class.stock_name)
            elif self.mode==1:
                raise NotImplementedError("Only MACD strategy implemented yet!")
                exit(-1)
    def map_operations_to_processes(self):
        #func_with_shared=partial(self.read_data,shared_list=self.shared_list)
        #self.process_pool.starmap(self.read_data,self.stock_name_chunks)
        for proc in self.process_pool:
            proc.start()
        proc.join()
        
class CalculateDataImplementation(ReadInstances):
    def __init__(self,mode) -> None:
        super().__init__(mode)
        
    
    



    




    