# Generated by Django 3.0.5 on 2020-04-26 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_itemstable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemstable',
            name='emailId',
        ),
    ]
