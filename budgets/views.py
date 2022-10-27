from decimal import Decimal
from unicodedata import decimal

import pandas
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, connection
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import render, redirect

from .forms import ExpenditureForm, ExpenditureEditForm, CategoryForm, PeriodForm, PeriodEditForm, BalanceEditForm, \
    MonthlyGoalForm, MonthlyGoalEditForm
from .models import *
from .utils import *


# Create your views here.


def index(request):
    """Main page for budgets app."""
    if request.user.is_authenticated:
        period = BudgetsPeriod.objects.filter(Q(owner=request.user) & Q(start_day__lte=date.today())
                                              & Q(end_day__gte=date.today())).order_by('-period_id').first()
        categories = BudgetsCategory.objects.filter(owner=request.user)
        chart = None
        gauge_chart = None

        # if there is no current period:
        if period is None:
            is_period = False
            context = {'is_period': is_period}
        # if there is current period:
        else:
            page_color = f"secondary"
            is_period = True

            expenses = select_date_range(period, request)



            sum_of_expenses = expenses.aggregate(Sum('expenditure_amount'))['expenditure_amount__sum']

            if sum_of_expenses is None:
                sum_of_expenses = 0

            balance = BudgetsBalance.objects.get(period_id_budgets_period=period)
            period_length = (getattr(period, 'end_day') - getattr(period, 'start_day')).days
            days_passed = ((date.today() - getattr(period, 'start_day')).days) + 1
            money_saved = getattr(balance, 'amount') - sum_of_expenses
            average_over_the_period = round(sum_of_expenses / days_passed, 2)
            progress = f"{round((days_passed * 100)/period_length)}"
            estimated_savings = getattr(balance, 'amount') - (Decimal(average_over_the_period) * period_length)

            period_days = pandas.date_range(start=getattr(period, 'start_day'), end=getattr(period, 'end_day'))
            pd_df = pandas.DataFrame(data=period_days, columns=['full_dates'])

            expenses_df = pandas.DataFrame(expenses.values())
            categories_df = pandas.DataFrame(categories.values())

            # create chart when any expenses exists
            if expenses:

                expenses_df['category_id_budgets_category'] = \
                    expenses_df['category_id_budgets_category_id'].map(
                        categories_df.set_index('category_id')['category_name'])
                expenses_df.rename({'expenditure_id': 'expense', 'expenditure_amount': 'value',
                                    'expenditure_date': 'date', 'category_id_budgets_category': 'category'},
                                   axis=1, inplace=True)
                expenses_df['date'] = expenses_df['date'].astype('datetime64[ns]')

                pd_expenses_df = pandas.merge(pd_df, expenses_df, left_on='full_dates', right_on='date', how='left')

            else:
                print(f"No expenses - no chart")

            monthly_goals = BudgetsMonthlyGoal.objects.filter(period_id_budgets_period=period)

            # if monthly goals for this period are empty
            if not monthly_goals:
                is_goal = False
                if expenses:
                    # chart with expenses
                    chart = get_categories_bar_chart(pd_expenses_df)
                    # chart with budget
                    gauge_chart = get_budget_gauge_chart(balance, money_saved, sum_of_expenses)

                context1 = {'is_goal': is_goal, 'page_color': page_color, 'chart': chart}

            # if monthly goals for this period exists
            else:
                is_goal = True


                goals_dict = create_goals_dict(monthly_goals, period_length, days_passed, expenses)
                daily_average_goal = round(monthly_goals.aggregate(Sum('goal'))['goal__sum'] / period_length, 2)
                sum_of_goals = round(monthly_goals.aggregate(Sum('goal'))['goal__sum'])
                planned_savings = getattr(balance, 'amount') - sum_of_goals
                if expenses:
                    chart = get_categories_bar_chart(pd_expenses_df, daily_average_goal)
                    gauge_chart = get_budget_gauge_chart(balance, money_saved, sum_of_expenses, sum_of_goals)

                if average_over_the_period < daily_average_goal:
                    page_color = f"success"
                else:
                    page_color = f'danger'

                context1 = {'is_goal': is_goal, 'goals_dict': goals_dict, 'daily_average_goal': daily_average_goal,
                            'planned_savings': planned_savings, 'sum_of_goals': sum_of_goals,
                            'page_color': page_color, 'chart': chart, 'gauge_chart': gauge_chart}

            context = {'sum_of_expenses': sum_of_expenses, 'money_saved': money_saved,
                        'average_over_the_period': average_over_the_period, 'days_passed': days_passed,
                        'period_length': period_length, 'period': period, 'balance': balance,
                        'is_period': is_period, 'progress': progress, 'estimated_savings': estimated_savings,
                        'chart': chart, 'gauge_chart': gauge_chart}
            context.update(context1)

        return render(request, 'budgets/info.html', context)
    else:
        return render(request, 'budgets/index.html')


@login_required
def expenses(request):
    """Displaying all expenses from current period."""
    period = BudgetsPeriod.objects.filter(owner=request.user).order_by('-period_id').first()
    expenses = select_date_range(period, request)
    categories = BudgetsCategory.objects.filter(owner=request.user)
    pie_chart = None
    bar_chart = None

    if request.method != 'POST':
        form = ExpenditureForm(request=request)

        if len(expenses) > 0:
            period_days = pandas.date_range(start=getattr(period, 'start_day'), end=getattr(period, 'end_day'))
            pd_df = pandas.DataFrame(data=period_days, columns=['full_dates'])

            expenses_df = pandas.DataFrame(expenses.values())
            categories_df = pandas.DataFrame(categories.values())
            expenses_df['category_id_budgets_category'] = \
                expenses_df['category_id_budgets_category_id'].map(
                    categories_df.set_index('category_id')['category_name'])
            expenses_df.rename({'expenditure_id': 'expense', 'expenditure_amount': 'value',
                                'expenditure_date': 'date', 'category_id_budgets_category': 'category'},
                               axis=1, inplace=True)
            expenses_df['date'] = expenses_df['date'].astype('datetime64[ns]')

            pd_expenses_df = pandas.merge(pd_df, expenses_df, left_on='full_dates', right_on='date', how='left')

            pie_chart = get_pie_chart(expenses_df)
            bar_chart = get_bar_chart(pd_expenses_df)

    else:
        form = ExpenditureForm(data=request.POST, request=request)
        if form.is_valid():
            new_expense = form.save(commit=False)
            new_expense.owner = request.user
            new_expense.save()
            return redirect('budgets:expenses')

    context = {'form': form, 'expenses': expenses, 'pie_chart': pie_chart, 'bar_chart': bar_chart}
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
    categories = BudgetsCategory.objects.filter(Q(owner=request.user) & Q(category_active=True)).order_by('category_id')

    if request.method != 'POST':
        form = CategoryForm()
    else:
        form = CategoryForm(data=request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.owner = request.user
            new_category.category_active = True
            new_category.save()
            return redirect('budgets:categories')

    context = {'form': form, 'categories': categories}
    return render(request, 'budgets/categories.html', context)


@login_required()
def category_delete(request, category_id):
    category = BudgetsCategory.objects.get(category_id=category_id)
    category.category_active = False
    category.save()
    # try:
    #     category.delete()
    # except IntegrityError:
    #     messages.error(request, 'This category is used. It cannot be removed.')
    return redirect('budgets:categories')


@login_required()
def category_settings(request, category_id):
    """Settings view for editing category name."""
    category = BudgetsCategory.objects.get(category_id=category_id)

    if request.method != 'POST':
        form = CategoryForm(instance=category)

    else:
        form = CategoryForm(instance=category, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('budgets:categories')

    context = {'category': category, 'form': form}
    return render(request, 'budgets/category_settings.html', context)


@login_required()
def periods(request):
    periods = BudgetsPeriod.objects.filter(owner=request.user).order_by('-period_id')
    balances = BudgetsBalance.objects.filter(owner=request.user).select_related('period_id_budgets_period').order_by(
        '-period_id_budgets_period')
    print(balances.values())

    if request.method != 'POST':
        pform = PeriodForm()
        bform = BalanceEditForm()
        bform.fields['amount'].initial = 0
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

            # return redirect('budgets:periods')
            return redirect('budgets:goals', period_id=new_period.period_id)

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
        form.fields['goal'].initial = 0
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
