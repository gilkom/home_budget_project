# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Balance(models.Model):
    email_saver = models.OneToOneField('Saver', models.DO_NOTHING, db_column='email_saver', primary_key=True)
    period_id_period = models.ForeignKey('Period', models.DO_NOTHING, db_column='period_id_period')
    amount = models.SmallIntegerField()

    def __str__(self):
        return f"Balance: {self.amount}"

    class Meta:
        managed = False
        db_table = 'balance'
        unique_together = (('email_saver', 'period_id_period'),)


class Category(models.Model):
    category_id = models.SmallIntegerField(primary_key=True)
    category_name = models.CharField(max_length=-1)

    def __str__(self):
        return self.category_name

    class Meta:
        managed = False
        db_table = 'category'


class Expenditure(models.Model):
    expenditure_id = models.SmallIntegerField(primary_key=True)
    email_saver = models.ForeignKey('Saver', models.DO_NOTHING, db_column='email_saver', blank=True, null=True)
    category_id_category = models.ForeignKey(Category, models.DO_NOTHING, db_column='category_id_category', blank=True, null=True)
    expenditure_amount = models.SmallIntegerField()
    expenditure_date = models.DateField()
    description = models.CharField(max_length=-1, blank=True, null=True)

    def __str__(self):
        return f"Expenditure: {self.expenditure_amount}"

    class Meta:
        managed = False
        db_table = 'expenditure'


class MonthlyGoal(models.Model):
    email_saver = models.OneToOneField('Saver', models.DO_NOTHING, db_column='email_saver', primary_key=True)
    category_id_category = models.ForeignKey(Category, models.DO_NOTHING, db_column='category_id_category')
    period_id_period = models.ForeignKey('Period', models.DO_NOTHING, db_column='period_id_period')
    goal = models.CharField(max_length=-1)

    def __str__(self):
        return f"Goal: {self.goal}"

    class Meta:
        managed = False
        db_table = 'monthly_goal'
        unique_together = (('email_saver', 'category_id_category', 'period_id_period'),)


class Period(models.Model):
    period_id = models.SmallIntegerField(primary_key=True)
    email_saver = models.ForeignKey('Saver', models.DO_NOTHING, db_column='email_saver', blank=True, null=True)
    name = models.CharField(max_length=-1)
    start_day = models.DateField()
    end_day = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'period'


class Saver(models.Model):
    email = models.CharField(primary_key=True, max_length=-1)
    name = models.CharField(max_length=-1)
    password = models.CharField(max_length=-1)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = 'saver'
