from django.contrib import admin

from .models import BudgetsPeriod, BudgetsMonthlyGoal, BudgetsBalance, \
    BudgetsCategory, BudgetsExpenditure, BudgetsSaver


# Register your models here.
@admin.register(BudgetsSaver)
class BudgetsSaverAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id')
    list_filter = ('id', 'user_id')
    search_fields = ('id', 'user_id')


@admin.register(BudgetsPeriod)
class BudgetsPeriodAdmin(admin.ModelAdmin):
    list_display = ('period_id', 'name', 'start_day', 'end_day', 'id_budgets_saver')
    list_filter = ('period_id', 'name', 'start_day', 'end_day', 'id_budgets_saver')
    search_fields = ('period_id', 'name', 'start_day', 'end_day', 'id_budgets_saver')


@admin.register(BudgetsMonthlyGoal)
class BudgetsMonthlyGoal(admin.ModelAdmin):
    list_display = ('goal', 'category_id_budgets_category', 'period_id_budgets_period', 'id_budgets_saver')
    list_filter = ('goal', 'category_id_budgets_category', 'period_id_budgets_period', 'id_budgets_saver')
    search_fields = ('goal', 'category_id_budgets_category', 'period_id_budgets_period', 'id_budgets_saver')

@admin.register(BudgetsBalance)
class BudgetsBalance(admin.ModelAdmin):
    list_display = ('amount', 'period_id_budgets_period', 'id_budgets_saver')
    list_filter = ('amount', 'period_id_budgets_period', 'id_budgets_saver')
    search_fields = ('amount', 'period_id_budgets_period', 'id_budgets_saver')


@admin.register(BudgetsCategory)
class BudgetsCategory(admin.ModelAdmin):
    list_display = ('category_id', 'category_name')
    list_filter = ('category_id', 'category_name')
    search_fields = ('category_id', 'category_name')


@admin.register(BudgetsExpenditure)
class BudgetsExpenditure(admin.ModelAdmin):
    list_display = ('expenditure_id', 'expenditure_amount', 'expenditure_date', 'description',
                    'category_id_budgets_category', 'id_budgets_saver')
    list_filter = ('expenditure_id', 'expenditure_amount', 'expenditure_date', 'description',
                    'category_id_budgets_category', 'id_budgets_saver')
    search_fields = ('expenditure_id', 'expenditure_amount', 'expenditure_date', 'description',
                    'category_id_budgets_category', 'id_budgets_saver')