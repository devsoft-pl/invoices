# Generated by Django 4.2.10 on 2024-02-28 21:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("invoices", "0026_alter_year_options_year_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="invoice",
            name="is_last_day",
            field=models.BooleanField(default=False, verbose_name="Last day in month"),
        ),
    ]
