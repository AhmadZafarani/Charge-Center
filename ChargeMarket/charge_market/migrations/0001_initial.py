# Generated by Django 4.0.6 on 2022-08-22 02:55

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('phone_number', models.CharField(max_length=11, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '09123456789'.", regex='^09\\d{9}$')])),
                ('charge', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('identifier', models.AutoField(primary_key=True, serialize=False)),
                ('_credit', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='SellTransaction',
            fields=[
                ('identifier', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.PositiveIntegerField()),
                ('phone_number', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='charge_market.phonenumber')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='charge_market.vendor')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ChargeTransaction',
            fields=[
                ('identifier', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.PositiveIntegerField()),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='charge_market.vendor')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
