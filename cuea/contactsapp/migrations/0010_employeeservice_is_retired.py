# Generated by Django 4.0.4 on 2022-06-06 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactsapp', '0009_alter_employeeservice_managers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeservice',
            name='is_retired',
            field=models.BooleanField(default=False),
        ),
    ]
