# Generated by Django 3.1.7 on 2021-04-27 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0004_auto_20210427_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentreg',
            name='studentimage',
            field=models.ImageField(blank=True, upload_to='static/studentImages/'),
        ),
    ]
