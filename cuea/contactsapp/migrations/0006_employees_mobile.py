# Generated by Django 4.0.4 on 2022-05-30 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactsapp', '0005_alter_employeevote_deshabhimani_sub'),
    ]

    operations = [
        migrations.AddField(
            model_name='employees',
            name='mobile',
            field=models.CharField(default=9125262266, max_length=20),
            preserve_default=False,
        ),
    ]
