from datetime import datetime, date

from django import forms

from budgets.models import BudgetsExpenditure, BudgetsPeriod, BudgetsCategory, BudgetsBalance, BudgetsMonthlyGoal


class ExpenditureForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request") # store value of request
        print(self.request.user)
        super().__init__(*args, **kwargs)
        self.fields['category_id_budgets_category'].queryset = BudgetsCategory.objects.filter(
            owner=self.request.user)

    expenditure_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date',
                                       'value': date.today().strftime("%Y-%m-%d")}), label='Date')

    class Meta:
        model = BudgetsExpenditure
        fields = ('expenditure_amount', 'expenditure_date', 'description', 'category_id_budgets_category')
        labels = {'expenditure_amount': 'Amount', 'category_id_budgets_category': 'Category'}


class ExpenditureEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request") # store value of request
        print(self.request.user)
        super().__init__(*args, **kwargs)
        self.fields['category_id_budgets_category'].queryset = BudgetsCategory.objects.filter(
            owner=self.request.user)

    expenditure_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),
                                       label='Date')

    class Meta:
        model = BudgetsExpenditure
        fields = ('expenditure_amount', 'expenditure_date', 'description', 'category_id_budgets_category')
        labels = {'expenditure_amount': 'Amount', 'expenditure_date': 'Date',
                  'category_id_budgets_category': 'Category'}


class CategoryForm(forms.ModelForm):

    class Meta:
        model = BudgetsCategory
        fields = ('category_name',)


class PeriodForm(forms.ModelForm):

    start_day = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),
                                       label='Date')
    end_day = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),
                                       label='Date')

    class Meta:
        model = BudgetsPeriod
        fields = ('name', 'start_day', 'end_day',)


class BalanceForm(forms.ModelForm):

    class Meta:
        model = BudgetsBalance
        fields = ('amount',)


class MonthlyGoalForm(forms.ModelForm):

    class Meta:
        model = BudgetsMonthlyGoal
        fields = ('category_id_budgets_category', 'goal',)
