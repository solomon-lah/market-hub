# Generated by Django 3.0.5 on 2020-04-28 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20200428_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertable',
            name='status',
            field=models.CharField(default='Allowed', max_length=7),
        ),
    ]
