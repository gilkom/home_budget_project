"""Wzorce adresów URL dla budgets."""
from django.urls import path

from . import views

app_name = 'budgets'
urlpatterns = [
    # Main page
    path('', views.index, name='index'),
    # Displaying all expenses list
    path('expenses/', views.expenses, name='expenses'),
    path('expenses/<int:expenditure_id>/', views.expenditure, name='expenditure'),
]