# Generated by Django 5.1.3 on 2024-12-24 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("invoices", "0031_alter_correctioninvoicerelation_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="invoice",
            options={"ordering": ["-sale_date"], "verbose_name_plural": "invoices"},
        ),
        migrations.AlterModelOptions(
            name="year",
            options={"ordering": ["-year"], "verbose_name_plural": "years"},
        ),
    ]
