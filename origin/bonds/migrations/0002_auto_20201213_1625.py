# Generated by Django 3.0.3 on 2020-12-13 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bonds', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bond',
            name='legal_name',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]