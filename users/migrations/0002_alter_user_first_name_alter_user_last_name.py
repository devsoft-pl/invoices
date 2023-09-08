# Generated by Django 4.2.4 on 2023-09-05 20:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(max_length=75, null=True, verbose_name="First name"),
        ),
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.CharField(max_length=75, null=True, verbose_name="Last name"),
        ),
    ]