# Generated by Django 3.2.15 on 2023-08-07 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0047_auto_20230807_1948'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.CharField(db_index=True, default='CASH', max_length=20, verbose_name='Cпособ оплаты'),
        ),
    ]
