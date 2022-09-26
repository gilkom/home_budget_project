import base64
from datetime import date
from io import BytesIO

from matplotlib import pyplot


from dateutil.relativedelta import relativedelta
from django.db.models import Q

from budgets.models import BudgetsExpenditure


def select_date_range(period, request):
    """Selecting last period or next 30 days"""
    if period.start_day <= date.today() <= period.end_day:
        expenses = BudgetsExpenditure.objects.filter(Q(owner=request.user) &
                                                     Q(expenditure_date__range=[period.start_day,
                                                                                period.end_day])).select_related('category_id_budgets_category').order_by(
            '-expenditure_date')
    else:
        expenses = BudgetsExpenditure.objects.filter(Q(owner=request.user) &
                                                     Q(expenditure_date__range=[date.today(),
                                                                                date.today() + relativedelta(
                                                                                    months=1)])).select_related('category_id_budgets_category').order_by(
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
    fig = pyplot.figure(figsize=(3, 3))
    key = 'category'
    d = data.groupby(key, as_index=False)['value'].agg('sum')
    pyplot.pie(data=d, x='value', labels=d[key], autopct='%1.0f%%', textprops={'fontsize': 16})
    pyplot.tight_layout()
    pie_chart = get_graph()
    return pie_chart


def get_bar_chart(data):
    pyplot.switch_backend('AGG')
    fig = pyplot.figure(figsize=(10, 4))
    key = 'date'
    d = data.groupby(key, as_index=False)['category'].agg('sum')
    pyplot.bar(d[key], d['category'])
    pyplot.tight_layout()
    bar_chart = get_graph()
    return bar_chart


