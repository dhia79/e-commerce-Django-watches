# Generated by Django 5.1 on 2024-09-12 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('DW', 'DRESS WATHCES'), ('SM', 'SMART WATCHES'), ('SW', 'SPORT WATCHES'), ('AW', 'AUTOMATIC WATCHES'), ('CW', 'CHRONOGRAPH WATCHES'), ('DV', 'DIVING WATCHES')], max_length=20),
        ),
    ]
