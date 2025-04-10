import decimal

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from num2words import num2words

from companies.models import Company
from currencies.models import Currency, ExchangeRate
from invoices.managers import InvoiceQuerySet
from persons.models import Person
from users.models import User


class Invoice(models.Model):
    INVOICE_SALES = 0
    INVOICE_PURCHASE = 1

    INVOICE_TYPES = (
        (INVOICE_SALES, _("Sales")),
        (INVOICE_PURCHASE, _("Purchase")),
    )

    BANK_TRANSFER = 0
    CASH_PAYMENT = 1

    PAYMENT_METHOD = (
        (BANK_TRANSFER, _("Transfer")),
        (CASH_PAYMENT, _("Cash")),
    )

    WEEKLY = 0
    BIWEEKLY = 1
    MONTHLY = 2
    THREE_MONTH = 3

    invoice_number = models.CharField(
        verbose_name=_("Invoice number"), max_length=30, null=True, blank=True
    )
    invoice_type = models.IntegerField(
        verbose_name=_("Invoice type"), choices=INVOICE_TYPES
    )
    company = models.ForeignKey(
        Company,
        verbose_name=_("Company"),
        on_delete=models.CASCADE,
        related_name="invoices",
        null=True,
        blank=True,
    )
    person = models.ForeignKey(
        Person,
        verbose_name=_("Person"),
        on_delete=models.CASCADE,
        related_name="invoices",
        null=True,
        blank=True,
    )
    is_recurring = models.BooleanField(verbose_name=_("Recurring"), default=False)
    is_last_day = models.BooleanField(
        verbose_name=_("Last day in month"), default=False
    )
    is_settled = models.BooleanField(verbose_name=_("Settled"), default=False)
    settlement_date = models.DateField(
        verbose_name=_("Settlement date"), default=timezone.now, editable=True
    )
    create_date = models.DateField(
        verbose_name=_("Create date"), default=timezone.now, editable=True
    )
    sale_date = models.DateField(
        verbose_name=_("Sale date"), default=timezone.now, editable=True
    )
    payment_date = models.DateField(
        verbose_name=_("Payment date"), default=timezone.now, editable=True
    )
    payment_method = models.IntegerField(
        verbose_name=_("Payment method"), choices=PAYMENT_METHOD, null=True, blank=True
    )
    currency = models.ForeignKey(
        Currency,
        verbose_name=_("Currency"),
        on_delete=models.CASCADE,
        null=True,
        related_name="invoices",
    )
    account_number = models.CharField(
        verbose_name=_("Account number"), max_length=50, null=True, blank=True
    )
    client = models.ForeignKey(
        Company,
        verbose_name=_("Client"),
        on_delete=models.CASCADE,
        related_name="client_invoices",
        null=True,
        blank=True,
    )
    invoice_file = models.FileField(
        verbose_name=_("Invoice file"), null=True, blank=True
    )
    is_paid = models.BooleanField(verbose_name=_("Paid"), default=False)
    net_amount = models.DecimalField(
        verbose_name=_("Net amount"), max_digits=9, decimal_places=2, default=0
    )
    gross_amount = models.DecimalField(
        verbose_name=_("Gross_amount"), max_digits=9, decimal_places=2, default=0
    )

    objects = InvoiceQuerySet.as_manager()

    class Meta:
        verbose_name_plural = _("invoices")
        ordering = ["-sale_date"]
        unique_together = ["invoice_number", "company"]

    def __str__(self):
        return self.invoice_number or f'{_("Recurring")}'

    def calculate_net_amount(self):
        net_sum = 0
        for item in self.items.all():
            net_sum = net_sum + item.net_amount
        return net_sum

    @property
    def tax_amount(self):
        tax_sum = 0
        for item in self.items.all():
            tax_sum = tax_sum + item.tax_amount
        return tax_sum

    def calculate_gross_amount(self):
        gross_sum = decimal.Decimal("0")
        for item in self.items.all():
            gross_sum = gross_sum + item.gross_amount
        return gross_sum

    @property
    def sell_rate_in_pln(self):
        exchange_rate = ExchangeRate.objects.get(
            date=self.sale_date, currency=self.currency
        )
        return exchange_rate.sell_rate

    @property
    def is_sell(self):
        return self.invoice_type == Invoice.INVOICE_SALES

    @property
    def has_item_with_vat(self):
        has_vat = False
        for item in self.items.all():
            if item.vat:
                has_vat = True

        return has_vat

    @property
    def has_items(self):
        return self.items.exists()

    @property
    def has_correction_invoice(self):
        return hasattr(self, "correction_invoice_relation")

    def get_html_for_pdf(self):
        items = self.items.all()

        template_path = "invoices/pdf_invoice.html"

        gross_amount = num2words(
            self.gross_amount,
            lang="pl",
            to="currency",
            currency=self.currency.code.upper(),
        )

        context = {
            "invoice": self,
            "items": items,
            "gross_amount": gross_amount,
        }

        html = render_to_string(template_path, context)
        return html


class Year(models.Model):
    year = models.PositiveSmallIntegerField(
        verbose_name=_("Year"),
    )
    user = models.ForeignKey(
        User, verbose_name=_("User"), on_delete=models.CASCADE, null=True
    )

    class Meta:
        verbose_name_plural = _("years")
        ordering = ["-year"]

    def __str__(self):
        return str(self.year)


@receiver(post_save, sender=Invoice)
def create_year_on_invoice(sender, instance: Invoice, created=False, **kwargs):
    Year.objects.get_or_create(year=instance.sale_date.year)


class CorrectionInvoiceRelation(models.Model):
    invoice = models.OneToOneField(
        Invoice,
        verbose_name=_("Invoice"),
        on_delete=models.CASCADE,
        related_name="original_invoice_relation",
    )
    correction_invoice = models.OneToOneField(
        Invoice,
        verbose_name=_("Correction Invoice"),
        on_delete=models.CASCADE,
        related_name="correction_invoice_relation",
    )

    class Meta:
        verbose_name_plural = _("correction invoices relation")

    def __str__(self):
        return (
            f"{self.invoice.invoice_number}, {self.correction_invoice.invoice_number}"
        )
