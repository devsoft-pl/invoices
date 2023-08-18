# Generated by Django 4.2.4 on 2023-08-18 10:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("companies", "0006_alter_company_nip_alter_company_regon"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="city",
            field=models.CharField(
                max_length=60,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[a-zA-Z]*$", "Enter the city in letters only"
                    )
                ],
                verbose_name="Miasto",
            ),
        ),
        migrations.AlterField(
            model_name="company",
            name="phone_number",
            field=models.CharField(
                blank=True,
                max_length=20,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[0-9]*$", "Enter phone number in numbers only"
                    )
                ],
                verbose_name="Numer telefonu",
            ),
        ),
        migrations.AlterField(
            model_name="company",
            name="zip_code",
            field=models.CharField(
                max_length=10,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[0-9]{2}-[0-9]{3}$", "Zip code in numbers only"
                    )
                ],
                verbose_name="Kod pocztowy",
            ),
        ),
    ]
