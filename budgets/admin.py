from django.contrib import admin

from .models import Saver, Period, MonthlyGoal, Balance, Category, Expenditure

# Register your models here.
admin.site.register(Saver)
admin.site.register(Period)
admin.site.register(MonthlyGoal)
admin.site.register(Balance)
admin.site.register(Category)
admin.site.register(Expenditure)
