# Generated by Django 4.2 on 2023-06-15 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_order_complete'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
    ]