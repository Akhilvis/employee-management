# Generated by Django 4.0.4 on 2022-05-27 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pf_number', models.IntegerField()),
                ('name', models.CharField(max_length=50)),
                ('blood_group', models.CharField(max_length=10)),
                ('adddress', models.TextField()),
                ('district', models.CharField(max_length=20)),
                ('pan_mun_cop', models.CharField(max_length=20)),
                ('pin_code', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeService',
            fields=[
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='contactsapp.employees')),
                ('designation', models.CharField(max_length=50)),
                ('department', models.CharField(max_length=50)),
                ('membership', models.CharField(choices=[('Association', 'Association'), ('Union', 'Union'), ('Neuatral', 'Neuatral')], default='Neuatral', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeVote',
            fields=[
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='contactsapp.employees')),
                ('legislative_assembly', models.CharField(max_length=30)),
                ('loksabha_constituency', models.CharField(max_length=30)),
                ('voters_id', models.CharField(max_length=30)),
                ('deshabhimani_sub', models.BooleanField(default=False)),
                ('subscription_amount', models.IntegerField()),
            ],
        ),
    ]
