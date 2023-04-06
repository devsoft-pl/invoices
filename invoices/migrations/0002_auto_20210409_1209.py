# Generated by Django 3.2 on 2021-04-09 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='city',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='company',
            name='default_currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='invoices.currency', verbose_name='Default currency'),
        ),
        migrations.AlterField(
            model_name='company',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='company',
            name='nip',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='NIP'),
        ),
        migrations.AlterField(
            model_name='company',
            name='street',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Street'),
        ),
        migrations.AlterField(
            model_name='company',
            name='zip_code',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='ZIP Code'),
        ),
        migrations.AlterField(
            model_name='currency',
            name='code',
            field=models.CharField(max_length=10, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='currency',
            name='symbol',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Symbol'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoices.company', verbose_name='Company'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='create_date',
            field=models.DateField(blank=True, null=True, verbose_name='Create date'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='currency',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='invoices.currency', verbose_name='Currency'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_number',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Invoice number'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_type',
            field=models.IntegerField(blank=True, choices=[(0, 'Sales'), (1, 'Purchase')], null=True, verbose_name='Invoice type'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='payment_date',
            field=models.DateField(blank=True, null=True, verbose_name='Payment date'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='payment_method',
            field=models.IntegerField(blank=True, choices=[(0, 'Transfer'), (1, 'Cash')], null=True, verbose_name='Payment method'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='sale_date',
            field=models.DateField(blank=True, null=True, verbose_name='Sale date'),
        ),
        migrations.AlterField(
            model_name='item',
            name='amount',
            field=models.PositiveIntegerField(verbose_name='Amount'),
        ),
        migrations.AlterField(
            model_name='item',
            name='invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoices.invoice', verbose_name='Invoice'),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='item',
            name='net_price',
            field=models.PositiveIntegerField(verbose_name='Net price'),
        ),
        migrations.AlterField(
            model_name='item',
            name='vat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoices.vatrate', verbose_name='Vat'),
        ),
        migrations.AlterField(
            model_name='vatrate',
            name='rate',
            field=models.PositiveIntegerField(verbose_name='Rate'),
        ),
    ]
