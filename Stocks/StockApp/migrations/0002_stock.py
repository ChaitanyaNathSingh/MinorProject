# Generated by Django 4.1.2 on 2022-10-15 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StockApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('Stock_id', models.AutoField(primary_key=True, serialize=False)),
                ('Stock_name', models.CharField(max_length=100, unique=True)),
                ('Stock_type', models.CharField(max_length=100)),
                ('Stock_about', models.CharField(max_length=1000)),
                ('Company_name', models.CharField(max_length=100)),
            ],
        ),
    ]
