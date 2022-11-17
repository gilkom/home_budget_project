import base64
import io
from collections import namedtuple
from math import ceil

import pandas
from datetime import date
from io import BytesIO

import matplotlib.pyplot as plt
import plotly.graph_objects as go

from dateutil.relativedelta import relativedelta
from django.db.models import Q, Sum
from plotly.offline import plot
from django.utils.translation import gettext_lazy as _

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


def get_budget_gauge_chart(balance, money_saved, sum_of_expenses, p_code, period, sum_of_goals=0):
    sum_of_goals = int(sum_of_goals)
    step = int(balance.amount) / 100
    start = period.start_day.strftime('%d.%m.%Y')
    fig = go.Figure(go.Indicator(
        title={'text': f"Okres: { period.start_day.strftime('%d.%m.%Y') } - { period.end_day.strftime('%d.%m.%Y')}", 'font': {'size': 12}},
        mode="gauge+number+delta",
        value=sum_of_expenses,
        number={'valueformat': 'f', 'suffix': str(' ' + _('Currency'))},
        domain={'x': [0, 1], 'y': [0, 1]},
        delta={'reference': -(sum_of_goals - 2*(sum_of_expenses)), 'increasing': {'symbol': str(_('plotlyLeft'))},
               'decreasing': {'symbol': str(_('plotlyExceeded'))}},
        gauge={
            'axis': {'range': [None, int(balance.amount)],
                     'nticks': 8,
                     'tickmode': 'auto',
                     'ticklen': 5,
                     'ticks': 'outside',
                     'tickfont': {'size': 8},

                     },
            'bar': {'color': "black"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [sum_of_goals + (step * 4), int(balance.amount)], 'color': '#FF0000'},
                {'range': [sum_of_goals + (step * 2), sum_of_goals + (step * 5)], 'color': '#FF5500'},
                {'range': [sum_of_goals + (step * 1), sum_of_goals + (step * 3)], 'color': '#FF9900'},
                {'range': [sum_of_goals - (step * 1), sum_of_goals + (step * 1)], 'color': '#FFFE00'},
                {'range': [sum_of_goals - (step * 4), sum_of_goals - (step * 1)], 'color': '#ADEE00'},
                {'range': [sum_of_goals - (step * 6), sum_of_goals - (step * 3)], 'color': '#5BDE00'},
                {'range': [0, sum_of_goals - (step * 5)], 'color': '#09CE00'}],
            'threshold': {
                'line': {'color': "black", 'width': 2},
                'thickness': 0.75,
                'value': sum_of_goals}}))
    fig.update_layout(
        paper_bgcolor=p_code,
        autosize=False,
        width=280,
        height=180,
        margin=go.layout.Margin(
            l=25,
            r=25,
            b=10,
            t=20,
            pad=5
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


def create_goals_dict(monthly_goals, period_length, days_passed, expenses, days_left):
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
        money_goal_left = m_g.goal - cat_sum
        money_per_category_per_day_left = round(money_goal_left / days_left, 2)

        category_color = create_colors_category(money_goal_left, money_per_category_per_day_left, av_daily_goal)

        goals_d = {m_g.monthly_goal_id: {'name': m_g.category_id_budgets_category,
                                         'goal': m_g.goal,
                                         'category_sum': cat_sum,
                                         'av_period': av_period_goal,
                                         'av_daily': av_daily_goal,
                                         'money_goal_left': money_goal_left,
                                         'money_per_category_per_day_left': money_per_category_per_day_left,
                                         'category_color': category_color}}
        goals_dict.update(goals_d)

    return goals_dict

def create_colors(item, lower=0, greater=0):
    color = "#f8f9fa"

    if lower is 0 and greater is 0:
        if item >= 0:
            color = "#d4edda"
        else:
            color = "#f8d7da"
    elif lower is not 0 and greater is 0:
        if item <= lower:
            color = "#d4edda"
        else:
            color = "#f8d7da"
    else:
        if item >= greater:
            color = "#d4edda"
        else:
            color = "#f8d7da"

    return color

def create_colors_category(money_left, money_per_day_left, daily_average_goal):
    color = "#f8f9fa"

    if money_left < 0:
        color = "#dc3545"
    else:
        if money_per_day_left >= daily_average_goal:
            color = "#d4edda"
        else:
            color = "#f8d7da"

    return color

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
