import base64
import pandas
from datetime import date
from io import BytesIO

from matplotlib import pyplot
import matplotlib.dates as mdates

from dateutil.relativedelta import relativedelta
from django.db.models import Q

from budgets.models import BudgetsExpenditure


def select_date_range(period, request):
    """Selecting last period or next 30 days"""
    if period is not None:
        if period.start_day <= date.today() <= period.end_day:
            expenses = BudgetsExpenditure.objects.filter(Q(owner=request.user) &
                                                         Q(expenditure_date__range=[period.start_day,
                                                                                    period.end_day])).select_related(
                'category_id_budgets_category').order_by(
                '-expenditure_date')
        else:
            expenses = BudgetsExpenditure.objects.filter(Q(owner=request.user) &
                                                         Q(expenditure_date__range=[date.today(),
                                                                                    date.today() + relativedelta(
                                                                                        months=1)])).select_related(
                'category_id_budgets_category').order_by(
                '-expenditure_date')
    else:
        expenses = BudgetsExpenditure.objects.filter(Q(owner=request.user) &
                                                     Q(expenditure_date__range=[date.today(),
                                                                                date.today() + relativedelta(
                                                                                    months=1)])).select_related(
            'category_id_budgets_category').order_by(
            '-expenditure_date')
    return expenses


def get_graph():
    buffer = BytesIO()
    pyplot.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_pie_chart(data):
    pyplot.switch_backend('AGG')
    pyplot.style.use('seaborn-v0_8')
    fig = pyplot.figure(figsize=(3, 3))
    key = 'category'
    d = data.groupby(key, as_index=False)['value'].agg('sum')
    pyplot.pie(data=d, x='value', labels=d[key], autopct='%1.0f%%', textprops={'fontsize': 11})
    pyplot.title('Category distribution:')
    pyplot.tight_layout()
    pie_chart = get_graph()
    return pie_chart


def get_bar_chart(data):
    data["full_dates"] = pandas.to_datetime(data["full_dates"]).dt.strftime('%m-%d')
    data["date"] = pandas.to_datetime(data["date"]).dt.strftime('%d-%m-%Y')

    pyplot.switch_backend('AGG')
    fig = pyplot.figure(figsize=(6, 3))
    key = 'full_dates'
    d = data.groupby(key, as_index=False)['value'].agg('sum')

    pyplot.bar(d[key], d['value'])
    pyplot.title('Period expenses:', loc='left')
    pyplot.xlabel("Date")
    pyplot.xticks(rotation=65)
    pyplot.ylabel("Value")
    pyplot.xticks(data.full_dates)
    pyplot.style.use('seaborn-v0_8')
    pyplot.tight_layout()

    bar_chart = get_graph()
    return bar_chart


def create_goals_dict(monthly_goals, period_length, days_passed):
    goals_dict = {}
    for m_g in monthly_goals:
        av_period_goal = round(m_g.goal / period_length, 2)
        av_daily_goal = round(m_g.goal / days_passed, 2)
        goals_d = {m_g.monthly_goal_id: {'name': m_g.category_id_budgets_category,
                                         'goal': m_g.goal, 'av_period': av_period_goal,
                                         'av_daily': av_daily_goal}}
        goals_dict.update(goals_d)

    return goals_dict
