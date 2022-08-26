from django.shortcuts import render, redirect

from .forms import ExpenditureForm
from .models import *

# Create your views here.


def index(request):
    """Main page for budgets app."""
    return render(request, 'budgets/index.html')


def expenses(request):
    """Displaying all expenses from current period."""
    expenses = BudgetsExpenditure.objects.all()

    if request.method != 'POST':
        form = ExpenditureForm()
    else:
        form = ExpenditureForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('budgets:expenses')


    context = {'form': form, 'expenses': expenses}
    return render(request, 'budgets/expenses.html', context)


def expenditure(request, expenditure_id):
    """Displaying details of a specified expense."""
    expenditure = BudgetsExpenditure.objects.get(expenditure_id=expenditure_id)
    context = {'expenditure': expenditure}
    return render(request, 'budgets/expenditure.html', context)


def new_expenditure(request):
    """Add new expenditure"""
    if request.method != 'POST':
        form = ExpenditureForm()
    else:
        form = ExpenditureForm(date=request.POST)
        if form.is_valid():
            form.save()
            return redirect('budgets:expenses')

    context = {'form': form}
    return render(request, 'budgets/expenses.html', context)
