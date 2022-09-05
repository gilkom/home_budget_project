from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import ExpenditureForm, ExpenditureEditForm
from .models import *

# Create your views here.


def index(request):
    """Main page for budgets app."""
    return render(request, 'budgets/index.html')

@login_required
def expenses(request):
    """Displaying all expenses from current period."""
    expenses = BudgetsExpenditure.objects.all().order_by('expenditure_id')

    if request.method != 'POST':
        form = ExpenditureForm()
    else:
        form = ExpenditureForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('budgets:expenses')

    context = {'form': form, 'expenses': expenses}
    return render(request, 'budgets/expenses.html', context)

@login_required()
def expenditure(request, expenditure_id):
    """Displaying, editing and deleting details of a specified expense."""
    expenditure = BudgetsExpenditure.objects.get(expenditure_id=expenditure_id)

    if request.method != 'POST':
        form = ExpenditureEditForm(instance=expenditure)
    else:
        form = ExpenditureEditForm(instance=expenditure, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('budgets:expenses')

    context = {'expenditure': expenditure, 'form': form}
    return render(request, 'budgets/expenditure.html', context)


