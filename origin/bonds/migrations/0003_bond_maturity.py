# Generated by Django 3.0.3 on 2020-12-13 17:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bonds', '0002_auto_20201213_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='bond',
            name='maturity',
            field=models.DateField(default=datetime.date(2025, 1, 1)),
            preserve_default=False,
        ),
    ]
