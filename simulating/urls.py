from django.contrib import admin
from django.urls import path,include
from simulating import views

urlpatterns = [
    path('all/',views.get_all_stocks),
    path('<str:stock_name>/<str:strategy>/',views.calculated_stock)
]
