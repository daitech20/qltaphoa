# Generated by Django 4.1.1 on 2022-11-01 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_product_category_delete_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkout',
            name='payment_type',
            field=models.IntegerField(choices=[(0, 'Tien mat'), (1, 'Momo')], default=0),
        ),
    ]
