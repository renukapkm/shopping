# Generated by Django 5.0.4 on 2024-04-29 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_rename_reg_phnumber_registration_reg_phnum'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registration',
            name='reg_name',
        ),
    ]
