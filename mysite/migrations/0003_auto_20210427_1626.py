# Generated by Django 3.1.7 on 2021-04-27 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0002_auto_20210426_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentreg',
            name='dob',
            field=models.DateField(),
        ),
        migrations.AlterModelTable(
            name='facultyreg',
            table=None,
        ),
        migrations.AlterModelTable(
            name='studentreg',
            table=None,
        ),
    ]
