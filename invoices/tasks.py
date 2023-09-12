import calendar
import logging
from datetime import datetime, timedelta

from django.utils.translation import gettext as _

from base.celery import app
from invoices.models import Invoice

logger = logging.getLogger(__name__)


@app.task(name="create_invoices_for_recurring")
def create_invoices_for_recurring():
    logger.info("Trying to create invoices recurring")

    invoices = Invoice.objects.filter(is_recurring=True)

    date = datetime.today()

    month_range = calendar.monthrange(date.year, date.month)
    last_day = month_range[1]

    if last_day != date.day:
        return

    for invoice in invoices:
        payment_date = date + timedelta(
            days=(invoice.payment_date - invoice.sale_date).days
        )
        new_invoice = Invoice.objects.create(
            invoice_number=f"{date.month}/{date.year}",
            invoice_type=Invoice.INVOICE_SALES,
            company=invoice.company,
            is_recurring=False,
            create_date=date,
            sale_date=date,
            payment_date=payment_date,
            payment_method=Invoice.BANK_TRANSFER,
            currency=invoice.currency,
            account_number=invoice.account_number,
            client=invoice.client,
        )

        for item in invoice.items.all():
            item.pk = None
            item.invoice = new_invoice
            item.save()

        subject = _("New recurring invoice")
        content = _(
            "A new recurring invoice has been created\n"
            "Best regards,\n"
            "Invoice Manager"
        )

        invoice.user.send_email(subject, content)

