# Generated by Django 4.2.7 on 2023-11-29 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_orders_protsent_orders_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='period',
            field=models.IntegerField(blank=True, choices=[(3, 3), (6, 6), (12, 12)], null=True),
        ),
    ]
