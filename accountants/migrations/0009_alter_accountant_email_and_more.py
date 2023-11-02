# Generated by Django 4.2.5 on 2023-11-02 22:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("companies", "0010_delete_summaryrecipient"),
        ("accountants", "0008_remove_accountant_user_accountant_company"),
    ]

    operations = [
        migrations.AlterField(
            model_name="accountant",
            name="email",
            field=models.EmailField(max_length=254, verbose_name="Email"),
        ),
        migrations.AlterUniqueTogether(
            name="accountant",
            unique_together={("email", "company")},
        ),
    ]