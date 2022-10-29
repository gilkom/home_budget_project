import base64
import io
from collections import namedtuple

import pandas
from datetime import date
from io import BytesIO

import matplotlib.pyplot as plt
import plotly.graph_objects as go

from dateutil.relativedelta import relativedelta
from django.db.models import Q, Sum
from plotly.offline import plot

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
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_graph_plotly(fig):
    buffer = io.BytesIO()
    # plt.savefig(buffer, format='png')
    fig_svg = fig.to_image(format="svg")
    buffer.write(fig_svg)
    buffer.seek(0)
    graph = base64.b64encode(buffer.getvalue())
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_pie_chart(data):
    plt.switch_backend('AGG')
    plt.style.use('seaborn-v0_8')
    fig = plt.figure(figsize=(4, 4))
    key = 'category'
    d = data.groupby(key, as_index=False)['value'].agg('sum')
    plt.pie(data=d, x='value', labels=d[key], autopct='%1.0f%%', textprops={'fontsize': 11}, shadow=True)
    # plt.title('Category distribution:')
    plt.tight_layout()
    pie_chart = get_graph()
    return pie_chart


def get_bar_chart(data):
    data["full_dates"] = pandas.to_datetime(data["full_dates"]).dt.strftime('%m-%d')
    data["date"] = pandas.to_datetime(data["date"]).dt.strftime('%d-%m-%Y')

    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(8, 4))
    key = 'full_dates'
    d = data.groupby(key, as_index=False)['value'].agg('sum')

    plt.style.use('seaborn-paper')
    plt.bar(d[key], d['value'])
    # plt.title('Period expenses:', loc='left')
    # plt.xlabel("Date")
    plt.xticks(rotation=65)
    # pyplot.ylabel("Value")
    # pyplot.xticks(data.full_dates.unique())
    # print(plt.style.available)

    plt.tight_layout()

    bar_chart = get_graph()
    return bar_chart


def get_categories_bar_chart(data, daily_average_goal=None):
    data["full_dates"] = pandas.to_datetime(data["full_dates"]).dt.strftime('%m-%d')
    data["date"] = pandas.to_datetime(data["date"]).dt.strftime('%d-%m-%Y')
    plt.switch_backend('AGG')
    plt.style.use('seaborn-paper')
    fig = plt.figure(figsize=(8, 4))
    key = 'full_dates'
    d = data.groupby(key, as_index=False)['value'].agg('sum')
    plt.bar(d[key], d['value'])
    # plt.title('Period expenses:', loc='left')
    # plt.xlabel("Date")
    plt.xticks(rotation=65)

    if daily_average_goal is not None:
        plt.axhline(y=daily_average_goal, color='r', linestyle='dashed')
        averages = get_average_list(d)
        plt.plot(averages, c='red')

    plt.tight_layout()

    chart = get_graph()
    return chart


def get_budget_gauge_chart(balance, money_saved, sum_of_expenses, p_code, sum_of_goals=None):
    step = int(balance.amount) / 100

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=sum_of_expenses,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [None, int(balance.amount)], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#2a3f5f"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [sum_of_goals + (step * 6), int(balance.amount)], 'color': 'red'},
                {'range': [sum_of_goals + (step * 5), sum_of_goals + (step * 7)], 'color': '#D43200'},
                {'range': [sum_of_goals + (step * 4), sum_of_goals + (step * 6)], 'color': '#D47C00'},
                {'range': [sum_of_goals + (step * 3), sum_of_goals + (step * 5)], 'color': '#D4CC00'},
                {'range': [sum_of_goals + (step * 2), sum_of_goals + (step * 4)], 'color': '#747F00'},
                {'range': [sum_of_goals + (step * 1), sum_of_goals + (step * 3)], 'color': '#1E9001'},
                {'range': [0, sum_of_goals + (step * 2)], 'color': 'green'}],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': sum_of_goals}}))
    fig.update_layout(
        paper_bgcolor=p_code,
        autosize=False,
        width=300,
        height=150,
        margin=go.layout.Margin(
            l=5,
            r=5,
            b=20,
            t=20,
            pad=4
        )
    )

    # Getting HTML needed to render the plot.
    gauge_chart = plot({'data': fig}, config = {'displayModeBar': False}, output_type='div')
    return gauge_chart



def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def create_goals_dict(monthly_goals, period_length, days_passed,expenses):
    goals_dict = {}
    for m_g in monthly_goals:
        av_period_goal = round(m_g.goal / period_length, 2)

        val = m_g.category_id_budgets_category.category_id
        if expenses.values('category_id_budgets_category').order_by('category_id_budgets_category').annotate(total_amount=Sum('expenditure_amount')).filter(category_id_budgets_category=val).exists():
            category_sum = expenses.values('category_id_budgets_category').order_by('category_id_budgets_category').annotate(total_amount=Sum('expenditure_amount')).get(category_id_budgets_category=val)
            cat_sum = category_sum['total_amount']
        else:
            cat_sum = 0

        av_daily_goal = round(cat_sum / days_passed, 2)

        goals_d = {m_g.monthly_goal_id: {'name': m_g.category_id_budgets_category,
                                         'goal': m_g.goal,
                                         'category_sum': cat_sum,
                                         'av_period': av_period_goal,
                                         'av_daily': av_daily_goal}}
        goals_dict.update(goals_d)

    return goals_dict

def get_average_list(d):
    today = (date.today().strftime('%m-%d'))
    counter = 0
    sum = 0
    average = []
    for index, row in d.iterrows():
        counter += 1
        sum = sum + row['value']
        average.append(round(sum / counter, 2))
        if row['full_dates'] == today:
            break

    return average
