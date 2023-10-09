# Generated by Django 4.2.5 on 2023-10-05 18:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("companies", "0005_alter_company_city_alter_company_nip_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="city",
            field=models.CharField(max_length=60, verbose_name="Miasto"),
        ),
        migrations.AlterField(
            model_name="company",
            name="nip",
            field=models.CharField(max_length=13, verbose_name="NIP"),
        ),
        migrations.AlterField(
            model_name="company",
            name="phone_number",
            field=models.CharField(
                blank=True, max_length=20, null=True, verbose_name="Numer telefonu"
            ),
        ),
        migrations.AlterField(
            model_name="company",
            name="regon",
            field=models.CharField(max_length=14, null=True, verbose_name="Regon"),
        ),
        migrations.AlterField(
            model_name="company",
            name="zip_code",
            field=models.CharField(max_length=10, verbose_name="Kod pocztowy"),
        ),
    ]