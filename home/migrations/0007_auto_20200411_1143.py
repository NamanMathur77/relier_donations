# Generated by Django 3.0.3 on 2020-04-11 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_item_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='status',
            field=models.CharField(default='pending', max_length=100),
        ),
    ]