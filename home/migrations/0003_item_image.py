# Generated by Django 3.0.3 on 2020-02-29 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_item_date_posted'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='item_pics'),
        ),
    ]
