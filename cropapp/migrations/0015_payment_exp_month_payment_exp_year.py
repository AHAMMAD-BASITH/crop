# Generated by Django 5.1.4 on 2025-02-02 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cropapp', '0014_remove_payment_exp_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='exp_month',
            field=models.IntegerField(default=0, max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='exp_year',
            field=models.IntegerField(default=0, max_length=4),
            preserve_default=False,
        ),
    ]
