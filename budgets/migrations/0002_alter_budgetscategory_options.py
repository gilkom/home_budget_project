# Generated by Django 4.1 on 2022-08-26 14:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='budgetscategory',
            options={'managed': False, 'verbose_name_plural': 'budgets categories'},
        ),
    ]
