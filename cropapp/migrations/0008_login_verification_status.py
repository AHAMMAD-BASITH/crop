# Generated by Django 5.1.4 on 2025-05-02 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cropapp', '0007_remove_user_verification_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='login',
            name='verification_status',
            field=models.IntegerField(default=0),
        ),
    ]
