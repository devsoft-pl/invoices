# Generated by Django 5.1.3 on 2024-12-24 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("summary_recipients", "0006_alter_summaryrecipient_day"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="summaryrecipient",
            options={"verbose_name_plural": "summary recipients"},
        ),
    ]