# Generated by Django 5.1 on 2024-09-25 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("summary_recipients", "0004_alter_summaryrecipient_company_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="summaryrecipient",
            name="is_last_day",
            field=models.BooleanField(default=False, verbose_name="Last day in month"),
        ),
    ]
