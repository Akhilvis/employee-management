# Generated by Django 4.0.4 on 2022-06-14 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contactsapp', '0024_remove_employeeservice_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeservice',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contactsapp.section'),
        ),
    ]