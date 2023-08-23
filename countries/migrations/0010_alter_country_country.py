# Generated by Django 4.2.4 on 2023-08-23 18:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("countries", "0009_alter_country_country"),
    ]

    operations = [
        migrations.AlterField(
            model_name="country",
            name="country",
            field=models.CharField(
                max_length=30,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[a-zA-Z ]{2,}$", "Enter the country in letters only"
                    )
                ],
                verbose_name="Kraj",
            ),
        ),
    ]
