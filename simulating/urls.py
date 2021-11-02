from django.contrib import admin
from django.urls import path,include
from simulating import views

urlpatterns = [
    path('/',views.get_all_stocks),
]
