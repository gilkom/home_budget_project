from datetime import datetime, date

from django import forms

from budgets.models import BudgetsExpenditure, BudgetsPeriod


class ExpenditureForm(forms.ModelForm):
    expenditure_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date',
                                       'value': date.today().strftime("%Y-%m-%d")}), label='Date')

    class Meta:
        model = BudgetsExpenditure
        fields = ('expenditure_amount', 'expenditure_date', 'description', 'category_id_budgets_category',
                  'owner')
        labels = {'expenditure_amount': 'Amount', 'category_id_budgets_category': 'Category',
                  'owner': 'User'}


class ExpenditureEditForm(forms.ModelForm):
    expenditure_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),
                                       label='Date')
    class Meta:
        model = BudgetsExpenditure
        fields = ('expenditure_amount', 'expenditure_date', 'description', 'category_id_budgets_category')
        labels = {'expenditure_amount': 'Amount', 'expenditure_date': 'Date',
                  'category_id_budgets_category': 'Category'}