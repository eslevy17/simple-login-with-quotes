# Generated by Django 2.0.6 on 2018-06-22 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('python_belt', '0002_auto_20180622_1712'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='likes',
            field=models.ManyToManyField(related_name='liked_quotes', to='python_belt.User'),
        ),
    ]
