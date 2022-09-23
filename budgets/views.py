from datetime import date
from itertools import chain

from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Model, Q
from django.forms import formset_factory
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect

from .forms import ExpenditureForm, ExpenditureEditForm, CategoryForm, PeriodForm, PeriodEditForm, BalanceEditForm, \
    MonthlyGoalForm, MonthlyGoalEditForm
from .models import *

# Create your views here.


def index(request):
    """Main page for budgets app."""
    return render(request, 'budgets/index.html')

@login_required
def expenses(request):
    """Displaying all expenses from current period."""
    period = BudgetsPeriod.objects.filter(owner=request.user).order_by('-period_id')[0]

    if period.start_day <= date.today() <= period.end_day:
        expenses = BudgetsExpenditure.objects.filter(Q(owner=request.user) &
                                                 Q(expenditure_date__range=[period.start_day, period.end_day])).order_by('-expenditure_date')
    else:
        expenses = BudgetsExpenditure.objects.filter(Q(owner=request.user) &
                                                     Q(expenditure_date__range=[date.today(),
                                                                                date.today() + relativedelta(months=1)])).order_by(
            '-expenditure_date')

    if request.method != 'POST':
        form = ExpenditureForm(request=request)
    else:
        form = ExpenditureForm(data=request.POST, request=request)
        if form.is_valid():
            new_expense = form.save(commit=False)
            new_expense.owner = request.user
            new_expense.save()
            return redirect('budgets:expenses')

    context = {'form': form, 'expenses': expenses, 'range': range}
    return render(request, 'budgets/expenses.html', context)


@login_required()
def expense_delete(request, expenditure_id):
    expense = BudgetsExpenditure.objects.get(expenditure_id=expenditure_id)
    expense.delete()

    return redirect('budgets:expenses')


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
def category_delete(request, category_id):
    category = BudgetsCategory.objects.get(category_id=category_id)
    try:
        category.delete()
    except IntegrityError:
        messages.error(request, 'This category is used. It cannot be removed.')
    return redirect('budgets:categories')


@login_required()
def periods(request):

    periods = BudgetsPeriod.objects.filter(owner=request.user).order_by('-period_id')
    balances = BudgetsBalance.objects.filter(owner=request.user).select_related('period_id_budgets_period').order_by('-period_id_budgets_period')

    if request.method != 'POST':
        pform = PeriodForm()
        bform = BalanceEditForm()
    else:
        pform = PeriodForm(request.POST)
        bform = BalanceEditForm(request.POST)

        if pform.is_valid() and bform.is_valid():

            new_period = pform.save(commit=False)
            new_period.owner = request.user
            new_period.save()
            new_balance = bform.save(commit=False)
            new_balance.owner = request.user
            new_balance.period_id_budgets_period = new_period
            new_balance.save()

            return redirect('budgets:periods')

    context = {'pform': pform, 'bform': bform, 'periods': periods, 'balances': balances}
    return render(request, 'budgets/periods.html', context)


@login_required()
def period_delete(request, period_id):
    period = BudgetsPeriod.objects.get(period_id=period_id)
    period.delete()
    return redirect('budgets:periods')


@login_required()
def period_settings(request, period_id):
    """Settings view for period and its balance and categories."""
    balance = BudgetsBalance.objects.get(period_id_budgets_period=period_id)
    period = BudgetsPeriod.objects.get(period_id=period_id)

    if request.method != 'POST':
        pform = PeriodEditForm(instance=period)
        bform = BalanceEditForm(instance=balance)

    else:
        pform = PeriodEditForm(instance=period, data=request.POST)
        bform = BalanceEditForm(instance=balance, data=request.POST)

        if bform.is_valid() and pform.is_valid():
            pform.save()
            bform.save()
            return redirect('budgets:periods')

    context = {'period': period, 'pform': pform, 'bform': bform}
    return render(request, 'budgets/period_settings.html', context)


@login_required()
def goals(request, period_id):
    goals = BudgetsMonthlyGoal.objects.filter(Q(owner=request.user) & Q(period_id_budgets_period=period_id))
    period = BudgetsPeriod.objects.get(period_id=period_id)

    if request.method != 'POST':
        form = MonthlyGoalForm(request=request)
    else:
        form = MonthlyGoalForm(data=request.POST, request=request)
        if form.is_valid():

            new_goal = form.save(commit=False)
            new_goal.period_id_budgets_period = period
            new_goal.owner = request.user
            try:
                new_goal.save()
            except IntegrityError:
                messages.error(request, 'This category is already added...')

            return redirect('budgets:goals', period_id=period_id)


    context = {'form': form, 'goals': goals, 'period': period}
    return render(request, 'budgets/goals.html', context)

@login_required()
def goal_settings(request, period_id, goal_id):

    period = BudgetsPeriod.objects.get(period_id=period_id)
    goal = BudgetsMonthlyGoal.objects.get(monthly_goal_id=goal_id)

    if request.method != 'POST':
        form = MonthlyGoalEditForm(instance=goal)
    else:
        form = MonthlyGoalEditForm(instance=goal, data=request.POST)

        if form.is_valid():
            form.save()
            return redirect('budgets:goals', period_id=period_id)

    context = {'period': period, 'form': form, 'goal': goal}
    return render(request, 'budgets/goal_settings.html', context)


@login_required()
def goal_delete(request, period_id, goal_id):
    goal = BudgetsMonthlyGoal.objects.get(monthly_goal_id=goal_id)
    goal.delete()
    return redirect('budgets:goals', period_id=period_id)