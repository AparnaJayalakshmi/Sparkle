# Generated by Django 4.2 on 2023-05-25 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True)),
                ('discount_value', models.DecimalField(decimal_places=2, max_digits=8)),
                ('minimum_purchase', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('maximum_discount', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('active', models.BooleanField(default=True)),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]