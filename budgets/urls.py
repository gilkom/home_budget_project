"""Wzorce adresów URL dla budgets."""
from django.urls import path

from . import views

app_name = 'budgets'
urlpatterns = [
    # Main page
    path('', views.index, name='index')
]