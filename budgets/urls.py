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
    path('categories/', views.categories, name='categories'),
    path('periods/', views.periods, name='periods'),
    path('periods/<int:period_id>/', views.period_settings, name='period_settings'),
    path('periods/goals/<int:period_id>/', views.goals, name='goals'),
]