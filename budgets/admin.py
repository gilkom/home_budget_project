from django.contrib import admin

from .models import BudgetsPeriod, BudgetsMonthlyGoal, \
    BudgetsBalance, BudgetsCategory, BudgetsExpenditure, BudgetsSaver

# Register your models here.
admin.site.register(BudgetsSaver)
admin.site.register(BudgetsPeriod)
admin.site.register(BudgetsMonthlyGoal)
admin.site.register(BudgetsBalance)
admin.site.register(BudgetsCategory)
admin.site.register(BudgetsExpenditure)
