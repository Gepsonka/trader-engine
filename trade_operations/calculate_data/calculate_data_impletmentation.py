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

# TODO: comment up the file!!
# TODO: divide the data loading and the calculations on the data into the two classes defined

class ReadInstances:
    '''Class wich reads into each json file with the corresponding stock name.
    This is done by all the cores of the processor, each subprocess connected to a IPC container (multiprocessing.Manager)
    The data load works but i dunno if the implementation will, bc yesterday my laptop almost cauth on fire processing all the data on
    all 8 of my cores. So i will test this on my pc later.'''
    def __init__(self,mode=0) -> None:
        self.mode=mode

        self.stock_name_chunks=list(self.chunks(list(self.get_stock_names()),mp.cpu_count()))

        self.manager=mp.Manager()
        self.shared_list=self.manager.list()
        self.process_pool=[mp.Process(target=self.read_data,args=(self.stock_name_chunks[i],self.shared_list)) for i in range(mp.cpu_count())]
        
    def chunks(self,lst, n):
        """Divide lst into n-piece chunks."""
        splited = [lst[i::n] for i in range(n)]
        return splited
    
    def get_stock_names(self):
        path=os.path.join(os.getcwd(),'static/stocks')
        for filename in os.listdir(path):
            yield filename.split('_')[0]

    def read_data(self,chunk,shared_list):
        for x in chunk:
            if self.mode==0:
                shared_list.append(ShortTermMACD(x))
                print("Stock has been loaded successfully! "+ x)
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
    """Calculating the dataframes on all of the dataclasses on all of the processor cores in subprocesses
    data will be saved in ready_data/{strategy_identifier}/ dir"""
    def __init__(self,mode) -> None:
        super().__init__(mode)
        self.shared_list_chunks=self.chunks(self.shared_list,mp.cpu_count())
        self.implementiation_process_pool=[mp.Process(target=self.implement,args=(self.shared_list_chunks[i],self.shared_list)) for i in range(mp.cpu_count())]
    
    def calculate_on_data(self,lst):
        for stock_class in lst:
            stock_class.implement()
            print("Calculations done on: "+stock_class.stock_name)

    def implement(self):
        for process in self.implementiation_process_pool:
            process.start()
        process.join()
        
    
    



    




    