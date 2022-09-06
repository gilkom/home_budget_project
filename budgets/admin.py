from django.contrib import admin

from .models import BudgetsPeriod, BudgetsMonthlyGoal, BudgetsBalance, \
    BudgetsCategory, BudgetsExpenditure



@admin.register(BudgetsPeriod)
class BudgetsPeriodAdmin(admin.ModelAdmin):
    list_display = ('period_id', 'name', 'start_day', 'end_day', 'owner')
    list_filter = ('period_id', 'name', 'start_day', 'end_day', 'owner')
    search_fields = ('period_id', 'name', 'start_day', 'end_day', 'owner')


@admin.register(BudgetsMonthlyGoal)
class BudgetsMonthlyGoal(admin.ModelAdmin):
    list_display = ('goal', 'category_id_budgets_category', 'period_id_budgets_period', 'owner')
    list_filter = ('goal', 'category_id_budgets_category', 'period_id_budgets_period', 'owner')
    search_fields = ('goal', 'category_id_budgets_category', 'period_id_budgets_period', 'owner')

@admin.register(BudgetsBalance)
class BudgetsBalance(admin.ModelAdmin):
    list_display = ('amount', 'period_id_budgets_period', 'owner')
    list_filter = ('amount', 'period_id_budgets_period', 'owner')
    search_fields = ('amount', 'period_id_budgets_period', 'owner')


@admin.register(BudgetsCategory)
class BudgetsCategory(admin.ModelAdmin):
    list_display = ('category_id', 'category_name', 'owner')
    list_filter = ('category_id', 'category_name', 'owner')
    search_fields = ('category_id', 'category_name', 'owner')


@admin.register(BudgetsExpenditure)
class BudgetsExpenditure(admin.ModelAdmin):
    list_display = ('expenditure_id', 'expenditure_amount', 'expenditure_date', 'description',
                    'category_id_budgets_category', 'owner')
    list_filter = ('expenditure_id', 'expenditure_amount', 'expenditure_date', 'description',
                    'category_id_budgets_category', 'owner')
    search_fields = ('expenditure_id', 'expenditure_amount', 'expenditure_date', 'description',
                    'category_id_budgets_category', 'owner')