from django.contrib import admin
from django.urls import path,include
from simulating import views

urlpatterns = [
    path('all-stocks/',views.get_all_stocks),
]
