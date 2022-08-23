# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Balance(models.Model):
    email_saver = models.OneToOneField('Saver', models.DO_NOTHING, db_column='email_saver', primary_key=True)
    period_id_period = models.ForeignKey('Period', models.DO_NOTHING, db_column='period_id_period')
    amount = models.FloatField()

    class Meta:
        managed = False
        db_table = 'balance'
        unique_together = (('email_saver', 'period_id_period'),)


class Category(models.Model):
    category_id = models.SmallIntegerField(primary_key=True)
    category_name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'category'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Expenditure(models.Model):
    expenditure_id = models.SmallIntegerField(primary_key=True)
    email_saver = models.ForeignKey('Saver', models.DO_NOTHING, db_column='email_saver', blank=True, null=True)
    category_id_category = models.ForeignKey(Category, models.DO_NOTHING, db_column='category_id_category', blank=True, null=True)
    expenditure_amount = models.FloatField()
    expenditure_date = models.DateField()
    description = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expenditure'


class MonthlyGoal(models.Model):
    email_saver = models.OneToOneField('Saver', models.DO_NOTHING, db_column='email_saver', primary_key=True)
    category_id_category = models.ForeignKey(Category, models.DO_NOTHING, db_column='category_id_category')
    period_id_period = models.ForeignKey('Period', models.DO_NOTHING, db_column='period_id_period')
    goal = models.FloatField()

    class Meta:
        managed = False
        db_table = 'monthly_goal'
        unique_together = (('email_saver', 'category_id_category', 'period_id_period'),)


class Period(models.Model):
    period_id = models.SmallIntegerField(primary_key=True)
    email_saver = models.ForeignKey('Saver', models.DO_NOTHING, db_column='email_saver', blank=True, null=True)
    name = models.CharField(max_length=30)
    start_day = models.DateField()
    end_day = models.DateField()

    class Meta:
        managed = False
        db_table = 'period'


class Saver(models.Model):
    email = models.CharField(primary_key=True, max_length=30)
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'saver'
