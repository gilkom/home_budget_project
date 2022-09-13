from django.contrib.auth.decorators import login_required
from django.db.models import Model, Q
from django.forms import formset_factory
from django.http import Http404
from django.shortcuts import render, redirect

from .forms import ExpenditureForm, ExpenditureEditForm, CategoryForm, PeriodForm, PeriodEditForm, BalanceEditForm, \
    MonthlyGoalEditForm
from .models import *

# Create your views here.


def index(request):
    """Main page for budgets app."""
    return render(request, 'budgets/index.html')

@login_required
def expenses(request):
    """Displaying all expenses from current period."""
    expenses = BudgetsExpenditure.objects.filter(owner=request.user).order_by('expenditure_id')

    if request.method != 'POST':
        form = ExpenditureForm(request=request)
    else:
        form = ExpenditureForm(data=request.POST, request=request)
        if form.is_valid():
            new_expense = form.save(commit=False)
            new_expense.owner = request.user
            new_expense.save()
            return redirect('budgets:expenses')

    context = {'form': form, 'expenses': expenses}
    return render(request, 'budgets/expenses.html', context)


@login_required()
def expenditure(request, expenditure_id):
    """Displaying, editing and deleting details of a specified expense."""
    expenditure = BudgetsExpenditure.objects.get(expenditure_id=expenditure_id)

    if expenditure.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = ExpenditureEditForm(instance=expenditure, request=request)
    else:
        form = ExpenditureEditForm(instance=expenditure, data=request.POST, request=request)
        if form.is_valid():
            form.save()
            return redirect('budgets:expenses')

    context = {'expenditure': expenditure, 'form': form}
    return render(request, 'budgets/expenditure.html', context)


@login_required()
def categories(request):
    categories = BudgetsCategory.objects.filter(owner=request.user).order_by('category_id')

    if request.method != 'POST':
        form = CategoryForm()
    else:
        form = CategoryForm(data=request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.owner = request.user
            new_category.save()
            return redirect('budgets:categories')

    context = {'form': form, 'categories': categories}
    return render(request, 'budgets/categories.html', context)


@login_required()
def periods(request):

    periods = BudgetsPeriod.objects.filter(owner=request.user).order_by('-period_id')

    if request.method != 'POST':
        pform = PeriodForm()
    else:
        pform = PeriodForm(request.POST)

        if pform.is_valid():

            new_period = pform.save(commit=False)
            new_period.owner = request.user
            new_period.save()

            return redirect('budgets:periods')

    context = {'pform': pform, 'periods': periods}
    return render(request, 'budgets/periods.html', context)


@login_required()
def period_settings(request, period_id):
    """Settings view for period and its balance and categories."""
    balance = BudgetsBalance.objects.get(period_id_budgets_period=period_id)
    period = BudgetsPeriod.objects.get(period_id=period_id)
    category = BudgetsCategory.objects.filter(owner=request.user)

    if request.method != 'POST':
        pform = PeriodEditForm(instance=period)
        bform = BalanceEditForm(instance=balance)
        mformset = formset_factory(MonthlyGoalEditForm, extra=len(category))
        print(f"len-cat:{len(category)}")
        formset = mformset(initial = [{'category_name': x.category_name} for x in category])
    else:
        pform = PeriodEditForm(instance=period, data=request.POST)
        bform = BalanceEditForm(instance=balance, data=request.POST)
        if bform.is_valid() and pform.is_valid():
            pform.save()
            bform.save()
            return redirect('budgets:periods')

    context = {'period': period, 'pform': pform, 'bform': bform, 'formset': formset}
    return render(request, 'budgets/period_settings.html', context)

