# Generated by Django 4.2.1 on 2023-06-03 20:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("vat_rates", "0003_vatrate_is_my_vat_alter_vatrate_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="vatrate",
            name="is_my_vat",
        ),
        migrations.AlterField(
            model_name="vatrate",
            name="rate",
            field=models.PositiveIntegerField(verbose_name="Stawka vat"),
        ),
    ]
