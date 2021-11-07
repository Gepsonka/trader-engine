
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import multiprocessing as mp
import os
from trade_operations.stock_class.stock_class_base import Stock
from trade_operations.strategies.strategy_base import Strategy
from trade_operations.io_operations.download_data import SaveDataImplementation
from trade_operations.calculate_data.calculate_data_impletmentation import CalculateDataImplementation
# Create your views here.




@api_view(['GET'])
def get_all_stocks(request):
    '''View to fetch all the stock names'''
    return Response(Stock.get_all_stock_name())


@api_view(['GET'])
def calculated_stock(request,stock_name,strategy):
    if os.path.exists('static/pid.txt'): # FIXME: check pid and not that the file exists
        return Response({'error':'Data is reloaded and recalculated...'})

    if stock_name not in Stock.get_all_stock_name():
        return Response({'error':'We do not have this stock'},status=status.HTTP_400_BAD_REQUEST)
    
    if strategy!='MACD' and strategy!='MeanReversion':
        return Response({'error':'We do not apply this strategy to the stocks'},status=status.HTTP_400_BAD_REQUEST)

    stock=Stock(stock_name)
    stock.load_dataframe(strategy)

    if strategy=='MACD':
        return Response(stock.convert_calculated_data_to_json(),status=status.HTTP_200_OK)
    elif strategy=='MeanReversion':
        return Response(stock.convert_calculated_data_to_json(1),status=status.HTTP_200_OK)




@api_view(['GET'])
def recalculate_data(request):
    def recalculate_data_proc():
        #dwnld=SaveDataImplementation('5y')
        #calc_MACD=CalculateDataImplementation()
        calc_MR=CalculateDataImplementation(1)
        #calc_MACD.implement_data_read()
        calc_MR.implement_data_read()
        if os.path.exists('static/pid.txt'):
            os.remove('static/pid.txt')

    if os.path.exists('static/pid.txt'): # FIXME: check pid and not that the file exists
        return Response({'error':'Data is reloaded and recalculated...'})
    p=mp.Process(target=recalculate_data_proc)
    p.start()
    with open('static/pid.txt','w') as file:
        file.write(str(p.pid))
    
    return Response({'succes':'Process started with an pid of: '+str(p.pid)})
