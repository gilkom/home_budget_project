from django import forms

from budgets.models import BudgetsExpenditure


class ExpenditureForm(forms.ModelForm):
    class Meta:
        model = BudgetsExpenditure
