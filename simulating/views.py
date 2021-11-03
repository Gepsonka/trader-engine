from django.shortcuts import render
from pandas.io import api
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import csv
from trade_operations.stock_class.stock_class_base import Stock
# Create your views here.

@api_view(['GET'])
def get_all_stocks(request):
    '''View to fetch all the stock names'''
    return Response(Stock.get_all_stock_name())


@api_view(['GET'])
def calculated_stock(request,stock_name,strategy):
    if stock_name not in Stock.get_all_stock_name():
        return Response({'error':'We do not have this stock'},status=status.HTTP_400_BAD_REQUEST)
    
    if strategy!='MACD' and strategy!='MeanReversion':
        print(strategy=='MACD')
        return Response({'error':'We do not apply this strategy to the stocks'},status=status.HTTP_400_BAD_REQUEST)

    stock=Stock(stock_name)
    stock.load_dataframe(strategy)

    return Response(stock.convert_calculated_data_to_json(),status=status.HTTP_200_OK)
