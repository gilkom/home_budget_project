from datetime import date

from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
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
    balance_id = models.BigAutoField(primary_key=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    period_id_budgets_period = models.ForeignKey('BudgetsPeriod', on_delete=models.CASCADE, db_column='period_id_budgets_period')
    owner = models.OneToOneField(User, models.DO_NOTHING, db_column='owner')

    def __str__(self):
        return f"Balance: {self.amount}"

    class Meta:
        managed = False
        db_table = 'budgets_balance'


class BudgetsCategory(models.Model):
    category_id = models.BigAutoField(primary_key=True)
    category_name = models.CharField(max_length=20)
    category_active = models.BooleanField()
    owner = models.ForeignKey(User, models.DO_NOTHING, db_column='owner')

    def __str__(self):
        return self.category_name

    class Meta:
        managed = False
        db_table = 'budgets_category'
        verbose_name_plural = 'budgets categories'


class BudgetsExpenditure(models.Model):
    expenditure_id = models.BigAutoField(primary_key=True)
    expenditure_amount = models.DecimalField(validators=[MinValueValidator(0)], max_digits=8, decimal_places=2)
    expenditure_date = models.DateField(validators=[MaxValueValidator(limit_value=date.today)])
    description = models.CharField(max_length=40, blank=True, null=True)
    category_id_budgets_category = models.ForeignKey(BudgetsCategory, models.DO_NOTHING,
                                                     db_column='category_id_budgets_category')
    owner = models.ForeignKey(User, models.DO_NOTHING, db_column='owner')


    def __str__(self):
        return f"Expenditure: {self.expenditure_amount}"

    class Meta:
        managed = False
        db_table = 'budgets_expenditure'


class BudgetsMonthlyGoal(models.Model):
    monthly_goal_id = models.BigAutoField(primary_key=True)
    goal = models.DecimalField(max_digits=8, decimal_places=2)
    category_id_budgets_category = models.ForeignKey(BudgetsCategory, models.DO_NOTHING,
                                                     db_column='category_id_budgets_category')
    period_id_budgets_period = models.ForeignKey('BudgetsPeriod', on_delete=models.CASCADE,
                                                 db_column='period_id_budgets_period')
    owner = models.OneToOneField(User, models.DO_NOTHING, db_column='owner')


    def __str__(self):
        return f"Goal: {self.goal}"

    class Meta:
        managed = False
        db_table = 'budgets_monthly_goal'
        unique_together = ('category_id_budgets_category', 'period_id_budgets_period', 'owner')


class BudgetsPeriod(models.Model):
    period_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=30)
    start_day = models.DateField()
    end_day = models.DateField()
    owner = models.ForeignKey(User, models.DO_NOTHING, db_column='owner')


    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'budgets_period'

