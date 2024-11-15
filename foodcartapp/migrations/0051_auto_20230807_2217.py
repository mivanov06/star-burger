# Generated by Django 3.2.15 on 2023-08-07 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0050_order_restaurant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='comment',
            field=models.TextField(blank=True, default='', max_length=1000, verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.CharField(choices=[('cash', 'Наличными при доставке'), ('online', 'Электронно при создании')], db_index=True, default='CASH', max_length=20, verbose_name='Cпособ оплаты'),
        ),
    ]
