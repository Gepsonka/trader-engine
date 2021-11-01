from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import csv
from trade_operations.stock_class.stock_class_base import Stock
# Create your views here.

@api_view(['GET'])
def get_all_stocks(request):
    '''View to fetch all the stock names'''
    stock_list=[]
    with open('static/500stock.csv') as file:
        csvfile=csv.reader(file)
        next(csvfile) # We do not need the header
        for row in csvfile:
            stock_list.append(row[0])
        
    return Response(stock_list)





