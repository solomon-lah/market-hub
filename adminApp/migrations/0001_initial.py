# Generated by Django 3.0.5 on 2020-04-28 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='loginForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adminId', models.CharField(max_length=20)),
                ('passcode', models.CharField(max_length=30)),
            ],
        ),
    ]
