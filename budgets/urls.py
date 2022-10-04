"""Wzorce adresów URL dla budgets."""
from django.urls import path

from . import views

app_name = 'budgets'
urlpatterns = [
    # Main page
    path('', views.index, name='index'),
    # Displaying all expenses list
    path('expenses/', views.expenses, name='expenses'),
    path('expense_delete/<int:expenditure_id>/', views.expense_delete, name='expense_delete'),
    path('expenses/<int:expenditure_id>/', views.expenditure, name='expenditure'),
    path('categories/', views.categories, name='categories'),
    path('category_delete/<int:category_id>', views.category_delete, name='category_delete'),
    path('categories/<int:category_id>/', views.category_settings, name='category_settings'),
    path('periods/', views.periods, name='periods'),
    path('period_delete/<int:period_id>', views.period_delete, name='period_delete'),
    path('periods/<int:period_id>/', views.period_settings, name='period_settings'),
    path('periods/<int:period_id>/goals/', views.goals, name='goals'),
    path('periods/<int:period_id>/goals/<int:goal_id>', views.goal_settings, name='goal_settings'),
    path('periods/<int:period_id>/goal_delete/<int:goal_id>', views.goal_delete, name='goal_delete'),
]