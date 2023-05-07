# Generated by Django 4.2 on 2023-05-07 16:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("countries", "0003_country_is_my_country_alter_country_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="country",
            name="country",
            field=models.CharField(max_length=30, verbose_name="Kraj"),
        ),
        migrations.AlterField(
            model_name="country",
            name="is_my_country",
            field=models.BooleanField(
                default=False, editable=False, verbose_name="Czy mój kraj"
            ),
        ),
    ]