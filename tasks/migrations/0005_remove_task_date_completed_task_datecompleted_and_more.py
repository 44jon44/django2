# Generated by Django 5.1.5 on 2025-01-23 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_rename_datecompleted_task_date_completed_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='date_completed',
        ),
        migrations.AddField(
            model_name='task',
            name='datecompleted',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
