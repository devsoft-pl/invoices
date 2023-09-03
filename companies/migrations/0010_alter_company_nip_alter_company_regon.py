# Generated by Django 4.2.4 on 2023-09-03 10:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("companies", "0009_alter_company_city_alter_company_email_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="nip",
            field=models.CharField(
                max_length=13,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[0-9a-zA-Z]{8,16}$",
                        "Wprowadź NIP bez znaków specjalnych, składający się z min. 8 znaków",
                    )
                ],
                verbose_name="NIP",
            ),
        ),
        migrations.AlterField(
            model_name="company",
            name="regon",
            field=models.CharField(
                max_length=14,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^([0-9]{9}|[0-9]{14})$",
                        "Regon należy wprowadzać wyłącznie cyframi składającymi się z min. 9 znaków",
                    )
                ],
                verbose_name="Regon",
            ),
        ),
    ]