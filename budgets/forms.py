from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from django import forms
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from budgets.models import BudgetsExpenditure, BudgetsPeriod, BudgetsCategory, BudgetsBalance, BudgetsMonthlyGoal


class ExpenditureForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request") # store value of request
        super().__init__(*args, **kwargs)
        self.fields['category_id_budgets_category'].queryset = BudgetsCategory.objects.filter(
            Q(owner=self.request.user) & Q(category_active=True))

    expenditure_date = forms.DateField(localize=True, widget=forms.DateInput(attrs={'type': 'date',
                                       'value': date.today().strftime("%Y-%m-%d")}), label=_('DateField'))

    class Meta:
        model = BudgetsExpenditure
        fields = ('expenditure_amount', 'expenditure_date', 'description', 'category_id_budgets_category')
        labels = {'expenditure_amount': _('AmountField'), 'category_id_budgets_category': _('Category')}


class ExpenditureEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request") # store value of request
        print(self.request.user)
        super().__init__(*args, **kwargs)
        self.fields['category_id_budgets_category'].queryset = BudgetsCategory.objects.filter(
            Q(owner=self.request.user) & Q(category_active=True))

    expenditure_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'BudgetsExpenditure'}),
                                       label=_('DateField'))

    class Meta:
        model = BudgetsExpenditure
        fields = ('expenditure_amount', 'expenditure_date', 'description', 'category_id_budgets_category')
        labels = {'expenditure_amount': _('AmountField'), 'category_id_budgets_category': _('Category')}


class CategoryForm(forms.ModelForm):

    class Meta:
        model = BudgetsCategory
        fields = ('category_name',)
        labels = {'category_name': _('Category'),}


class PeriodForm(forms.ModelForm):

    start_day = forms.DateField(widget=forms.DateInput(attrs={'type': 'date',
                                       'value': date.today().strftime("%Y-%m-%d")}), label=_('StartDateField'))

    # setting default end date to a month from today
    end_date = date.today() + relativedelta(months=1)
    current_end_date = end_date.strftime('%Y-%m-%d')
    end_day = forms.DateField(widget=forms.DateInput(attrs={'type': 'date',
                                       'value': current_end_date}), label=_('EndDateField'))

    class Meta:
        model = BudgetsPeriod
        fields = ('name', 'start_day', 'end_day',)
        labels = {'name': _('NameField'), }


class PeriodEditForm(forms.ModelForm):

    start_day = forms.DateField(widget=forms.DateInput(attrs={'class': 'BudgetsPeriod'}),
                                       label=_('StartDateField'))
    end_day = forms.DateField(widget=forms.DateInput(attrs={'class': 'BudgetsPeriod'}),
                                       label=_('EndDateField'))

    class Meta:
        model = BudgetsPeriod
        fields = ('name', 'start_day', 'end_day',)
        labels = {'name': _('NameField'), }


class BalanceEditForm(forms.ModelForm):

    class Meta:
        model = BudgetsBalance
        fields = ('amount', )
        labels = {'amount': _('PeriodBalanceField')}


class MonthlyGoalForm(forms.ModelForm):


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")  # store value of request
        super().__init__(*args, **kwargs)
        self.fields['category_id_budgets_category'].queryset = BudgetsCategory.objects.filter(
            Q(owner=self.request.user) & Q(category_active=True))

    class Meta:
        model = BudgetsMonthlyGoal
        fields = ('category_id_budgets_category', 'goal', )
        labels = {'category_id_budgets_category': _('Category'), 'goal': _('Goal')}


class MonthlyGoalEditForm(forms.ModelForm):

    class Meta:
        model = BudgetsMonthlyGoal
        fields = ('goal',)
        labels = {'goal': _('Goal'),}
