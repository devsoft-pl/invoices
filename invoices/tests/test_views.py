from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse

from invoices.factories import InvoiceFactory
from invoices.models import Invoice
from users.factories import UserFactory


class TestInvoice(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.user.set_password("test")
        self.user.save()
        self.user_invoices = sorted(
            InvoiceFactory.create_batch(12, user=self.user),
            key=lambda invoice: invoice.sale_date,
        )
        self.other_invoice = InvoiceFactory()


class TestListInvoices(TestInvoice):
    def setUp(self) -> None:
        super().setUp()
        self.url = reverse("invoices:list_invoices")

    def test_list_invoices_if_not_logged(self):
        response = self.client.get(self.url, follow=True)

        self.assertRedirects(response, f"/users/login/?next={self.url}")

    def test_list_invoices_if_logged(self):
        self.client.login(username=self.user.username, password="test")
        response = self.client.get(self.url)

        object_list = response.context["invoices"]

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "invoices/list_invoices.html")
        self.assertTrue(len(object_list) == 10)
        self.assertListEqual(list(object_list), self.user_invoices[:10])

    def test_list_invoices_second_pag(self):
        self.client.login(username=self.user.username, password="test")
        response = self.client.get(f"{self.url}?page=2")

        object_list = response.context["invoices"]

        self.assertTrue(len(object_list) == 2)
        self.assertListEqual(list(object_list), self.user_invoices[10:])


class TestDetailInvoice(TestInvoice):
    def setUp(self) -> None:
        super().setUp()
        self.invoice = self.user_invoices[0]
        self.url = reverse("invoices:detail_invoice", args=[self.invoice.pk])

    def test_detail_invoice_if_not_logged(self):
        response = self.client.get(self.url, follow=True)

        self.assertRedirects(response, f"/users/login/?next={self.url}")

    def test_detail_invoice_if_logged(self):
        self.client.login(username=self.user.username, password="test")
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "invoices/detail_invoice.html")
        self.assertEqual(self.invoice.pk, response.context["invoice"].pk)

    def rest_return_404_if_not_my_invoice(self):
        url = reverse("invoices:detail_invoice", args=[self.other_invoice.pk])
        self.client.login(username=self.user.username, password="test")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)


class TestDeleteInvoice(TestInvoice):
    def setUp(self) -> None:
        super().setUp()
        self.invoice = self.user_invoices[0]
        self.url = reverse("invoices:delete_invoice", args=[self.invoice.pk])

    def test_delete_invoice_if_not_logged(self):
        response = self.client.get(self.url, follow=True)

        self.assertRedirects(response, f"/users/login/?next={self.url}")

    def test_delete_invoice_if_logged(self):
        self.client.login(username=self.user.username, password="test")
        response = self.client.get(self.url)

        with self.assertRaises(ObjectDoesNotExist):
            Invoice.objects.get(pk=self.invoice.pk)
        self.assertEqual(response.status_code, 302)

    def rest_return_404_if_not_my_invoice(self):
        url = reverse("invoices:delete_invoice", args=[self.other_invoice.pk])
        self.client.login(username=self.user.username, password="test")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
