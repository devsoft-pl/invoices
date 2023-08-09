# Generated by Django 4.2.4 on 2023-08-07 19:56

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("invoices", "0005_remove_invoice_is_my_invoice"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="invoice",
            options={"ordering": ["-sale_date"]},
        ),
        migrations.AlterField(
            model_name="invoice",
            name="is_recurring",
            field=models.BooleanField(default=False, verbose_name="Cykliczna"),
        ),
        migrations.AlterUniqueTogether(
            name="invoice",
            unique_together={("invoice_number", "user")},
        ),
    ]