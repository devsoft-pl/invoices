# Generated by Django 4.1.7 on 2023-04-08 05:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("countries", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Company",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Name")),
                (
                    "nip",
                    models.CharField(max_length=12, unique=True, verbose_name="NIP"),
                ),
                (
                    "regon",
                    models.CharField(
                        max_length=12, null=True, unique=True, verbose_name="Regon"
                    ),
                ),
                ("address", models.CharField(max_length=100, verbose_name="Address")),
                ("zip_code", models.CharField(max_length=10, verbose_name="ZIP Code")),
                ("city", models.CharField(max_length=60, verbose_name="City")),
                ("email", models.EmailField(max_length=254, verbose_name="Email")),
                (
                    "phone_number",
                    models.CharField(
                        blank=True,
                        max_length=20,
                        null=True,
                        verbose_name="Phone number",
                    ),
                ),
                (
                    "country",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="countries.country",
                        verbose_name="Country",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="User",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "companies",
            },
        ),
    ]
