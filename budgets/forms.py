from datetime import datetime, date

from django import forms

from budgets.models import BudgetsExpenditure


class ExpenditureForm(forms.ModelForm):
    expenditure_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date',
                                       'value': date.today().strftime("%Y-%m-%d")}), label='Date')

    class Meta:
        model = BudgetsExpenditure
        fields = ('expenditure_amount', 'expenditure_date', 'description', 'category_id_budgets_category',
                  'id_budgets_saver')
        labels = {'expenditure_amount': 'Amount', 'category_id_budgets_category': 'Category',
                  'id_budgets_saver': 'User'}
