from decimal import Decimal

import pytest

from invoices.factories import InvoiceFactory
from items.factories import ItemFactory
from vat_rates.factories import VatRateFactory


@pytest.mark.django_db
class TestInvoiceModel:
    @pytest.fixture(autouse=True)
    def set_up(self):
        self.invoice = InvoiceFactory.create()
        self.invoice_2 = InvoiceFactory.create()
        vat = VatRateFactory.create(rate=23)
        self.item = ItemFactory.create(
            invoice=self.invoice, amount=2, net_price=1200, vat=vat
        )
        self.item_2 = ItemFactory.create(
            invoice=self.invoice, amount=1, net_price=800, vat=vat
        )

    def test_str_returns_item_name(self):
        assert self.invoice.__str__() == self.invoice.invoice_number

    def test_returns_net_sum(self):
        assert self.invoice.net_amount == Decimal("3200")

    def test_returns_zero_net_sum_if_no_items(self):
        assert self.invoice_2.net_amount == Decimal("0")

    def test_returns_tax_amount(self):
        assert self.invoice.tax_amount == Decimal("736")

    def test_returns_zero_tax_amount_if_no_items(self):
        assert self.invoice_2.tax_amount == Decimal("0")

    def test_returns_gross_amount(self):
        assert self.invoice.gross_amount == Decimal("3936")

    def test_returns_zero_gross_amount_if_no_items(self):
        assert self.invoice_2.gross_amount == Decimal("0")

    def test_returns_name_item(self):
        assert self.invoice.name_item == self.item.name

    def test_returns_pkwiu_item(self):
        assert self.invoice.pkwiu_item == self.item.pkwiu

    def test_returns_amount_item(self):
        assert self.invoice.amount_item == self.item.amount

    def test_returns_vat_item(self):
        assert self.invoice.vat_item == self.item.vat

    def test_returns_price_item(self):
        assert self.invoice.price_item() == self.item.net_price