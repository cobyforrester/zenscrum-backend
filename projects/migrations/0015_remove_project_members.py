# Generated by Django 2.2.13 on 2020-07-10 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0014_auto_20200710_1631'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='members',
        ),
    ]