# Generated by Django 4.2.5 on 2023-12-03 20:57

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("currencies", "0003_alter_currency_code"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="exchangerate",
            options={"verbose_name_plural": "exchange rates"},
        ),
    ]
