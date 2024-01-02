import datetime
from unittest.mock import patch

import pytest

from companies.factories import CompanyFactory
from currencies.factories import CurrencyFactory
from invoices.factories import InvoiceSellFactory, InvoiceSellPersonFactory
from invoices.models import Invoice
from invoices.tasks import (create_invoices_for_recurring,
                            send_monthly_summary_to_recipients)
from items.factories import ItemFactory
from summary_recipients.factories import SummaryRecipientFactory


@pytest.mark.django_db
class TestRecurrentInvoiceTasks:
    @pytest.fixture(autouse=True)
    def set_up(self) -> None:
        self.currency = CurrencyFactory.create(code="PLN")

    @patch("invoices.tasks.datetime")
    def test_creates_new_invoice_on_last_day_of_month(self, datetime_mock):
        invoice = InvoiceSellFactory.create(is_recurring=True, currency=self.currency)
        ItemFactory.create_batch(2, invoice=invoice)
        datetime_mock.today.return_value = datetime.date(2023, 8, 31)

        create_invoices_for_recurring()

        assert Invoice.objects.count() == 2
        assert (
            invoice.items.count()
            == Invoice.objects.get(is_recurring=False).items.count()
        )

    @patch("invoices.tasks.datetime")
    def test_creates_new_person_invoice_on_last_day_of_month(self, datetime_mock):
        person_invoice = InvoiceSellPersonFactory.create(
            is_recurring=True, currency=self.currency
        )
        ItemFactory.create_batch(2, invoice=person_invoice)
        datetime_mock.today.return_value = datetime.date(2023, 8, 31)

        create_invoices_for_recurring()

        assert Invoice.objects.count() == 2
        assert (
            person_invoice.items.count()
            == Invoice.objects.get(is_recurring=False).items.count()
        )

    @patch("invoices.tasks.datetime")
    def test_not_creates_new_invoice_if_not_last_day_of_month(self, datetime_mock):
        InvoiceSellFactory.create(is_recurring=True, currency=self.currency)
        datetime_mock.today.return_value = datetime.date(2023, 8, 15)

        create_invoices_for_recurring()

        assert Invoice.objects.count() == 1


@pytest.mark.django_db
class TestSummaryRecipientTasks:
    @pytest.fixture(autouse=True)
    def set_up(self) -> None:
        self.today = datetime.datetime.today()
        self.last_month_date = self.today - datetime.timedelta(days=self.today.day)
        self.last_month_date_2 = self.last_month_date.replace(day=7)
        self.company = CompanyFactory.create(is_my_company=True)
        self.currency = CurrencyFactory.create(code="PLN")
        self.invoice_1 = InvoiceSellFactory.create(
            company=self.company,
            create_date=self.last_month_date,
            is_settled=False,
            currency=self.currency,
        )
        self.invoice_2 = InvoiceSellFactory.create(
            company=self.company,
            create_date=self.last_month_date_2,
            currency=self.currency,
        )

    @patch("summary_recipients.models.SummaryRecipient.send_email")
    def test_send_monthly_summary_in_defined_day(self, send_email_mock):
        SummaryRecipientFactory.create(company=self.company, day=self.today.day)

        send_monthly_summary_to_recipients()

        send_email_mock.assert_called()
        files = send_email_mock.call_args[0][2]
        assert len(files) == 2

    @patch("summary_recipients.models.SummaryRecipient.send_email")
    def test_not_send_monthly_summary_if_another_day_other_than_defined_day(
        self, send_email_mock
    ):
        SummaryRecipientFactory.create(company=self.company)

        send_monthly_summary_to_recipients()

        send_email_mock.assert_not_called()

    @pytest.mark.parametrize(
        "final_call, expected_value", [[True, True], [False, False]]
    )
    def test_if_invoice_is_settled_on_final_call(self, final_call, expected_value):
        SummaryRecipientFactory.create(
            company=self.company, day=self.today.day, final_call=final_call
        )

        send_monthly_summary_to_recipients()
        self.invoice_1.refresh_from_db()

        assert self.invoice_1.is_settled is expected_value
