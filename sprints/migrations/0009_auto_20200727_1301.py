# Generated by Django 2.2.13 on 2020-07-27 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sprints', '0008_auto_20200726_2113'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sprint',
            options={'ordering': ['id']},
        ),
        migrations.RemoveField(
            model_name='sprint',
            name='number',
        ),
    ]
