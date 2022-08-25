from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class BudgetsBalance(models.Model):
    amount = models.FloatField()
    period_id_budgets_period = models.ForeignKey('BudgetsPeriod', models.DO_NOTHING, db_column='period_id_budgets_period')
    id_budgets_saver = models.OneToOneField('BudgetsSaver', models.DO_NOTHING, db_column='id_budgets_saver', primary_key=True)

    def __str__(self):
        return f"Balance: {self.amount}"

    class Meta:
        managed = False
        db_table = 'budgets_balance'
        unique_together = (('id_budgets_saver', 'period_id_budgets_period'),)


class BudgetsCategory(models.Model):
    category_id = models.SmallAutoField(primary_key=True)
    category_name = models.CharField(max_length=20)

    def __str__(self):
        return self.category_name

    class Meta:
        managed = False
        db_table = 'budgets_category'


class BudgetsExpenditure(models.Model):
    expenditure_id = models.BigAutoField(primary_key=True)
    expenditure_amount = models.FloatField()
    expenditure_date = models.DateField()
    description = models.CharField(max_length=300, blank=True, null=True)
    category_id_budgets_category = models.ForeignKey(BudgetsCategory, models.DO_NOTHING, db_column='category_id_budgets_category', blank=True, null=True)
    id_budgets_saver = models.ForeignKey('BudgetsSaver', models.DO_NOTHING, db_column='id_budgets_saver', blank=True, null=True)


    def __str__(self):
        return f"Expenditure: {self.expenditure_amount}"

    class Meta:
        managed = False
        db_table = 'budgets_expenditure'


class BudgetsMonthlyGoal(models.Model):
    goal = models.FloatField()
    category_id_budgets_category = models.ForeignKey(BudgetsCategory, models.DO_NOTHING,
                                                     db_column='category_id_budgets_category')
    period_id_budgets_period = models.ForeignKey('BudgetsPeriod', models.DO_NOTHING,
                                                 db_column='period_id_budgets_period')
    id_budgets_saver = models.OneToOneField('BudgetsSaver', models.DO_NOTHING, db_column='id_budgets_saver',
                                            primary_key=True)


    def __str__(self):
        return f"Goal: {self.goal}"

    class Meta:
        managed = False
        db_table = 'budgets_monthly_goal'
        unique_together = (('id_budgets_saver', 'category_id_budgets_category', 'period_id_budgets_period'),)


class BudgetsPeriod(models.Model):
    period_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    start_day = models.DateField()
    end_day = models.DateField()
    id_budgets_saver = models.ForeignKey('BudgetsSaver', models.DO_NOTHING, db_column='id_budgets_saver', blank=True,
                                         null=True)


    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'budgets_period'


class BudgetsSaver(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        managed = False
        db_table = 'budgets_saver'

