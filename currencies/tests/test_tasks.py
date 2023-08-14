from datetime import datetime
from unittest.mock import call, patch

import pytest

from currencies.factories import CurrencyFactory, ExchangeRateFactory
from currencies.models import ExchangeRate
from currencies.tasks import get_exchange_rates_for_all
from users.factories import UserFactory


@pytest.mark.django_db
class TestExchangeRatesTasks:
    @pytest.fixture(autouse=True)
    def set_up(self) -> None:
        self.user = UserFactory.create()
        self.currency_usd = CurrencyFactory.create(user=self.user, code="USD")
        self.currency_eur = CurrencyFactory.create(user=self.user, code="eur")
        self.buy_rate = "3.9758"
        self.sell_rate = "4.0562"

    @patch("currencies.nbp.adapter.NBPExchangeRatesAdapter.get_currency_buy_rate")
    @patch("currencies.nbp.adapter.NBPExchangeRatesAdapter.get_currency_sell_rate")
    def test_get_exchange_rates_when_buy_rate_and_sell_rate_exists(
        self, get_currency_buy_rate_mock, get_currency_sell_rate_mock
    ):
        get_currency_buy_rate_mock.return_value = self.buy_rate
        get_currency_sell_rate_mock.return_value = self.sell_rate

        ExchangeRateFactory(currency=self.currency_usd, date=datetime.today())

        get_exchange_rates_for_all()

        assert get_currency_buy_rate_mock.call_count == 2
        assert get_currency_sell_rate_mock.call_count == 2

        assert get_currency_buy_rate_mock.call_args_list == [call("eur"), call("usd")]

        assert (
            ExchangeRate.objects.filter(
                date=datetime.today(), currency=self.currency_usd
            ).count()
            == 1
        )
        assert (
            ExchangeRate.objects.filter(
                date=datetime.today(), currency=self.currency_eur
            ).count()
            == 1
        )

    @patch("currencies.nbp.adapter.NBPExchangeRatesAdapter.get_currency_buy_rate")
    @patch("currencies.nbp.adapter.NBPExchangeRatesAdapter.get_currency_sell_rate")
    def test_get_exchange_rates_when_buy_rate_and_sell_rate_not_exists(
        self, get_currency_buy_rate_mock, get_currency_sell_rate_mock
    ):
        get_currency_buy_rate_mock.return_value = None
        get_currency_sell_rate_mock.return_value = None

        get_exchange_rates_for_all()

        assert (
            ExchangeRate.objects.filter(
                date=datetime.today(), currency=self.currency_usd
            ).count()
            == 0
        )
        assert (
            ExchangeRate.objects.filter(
                date=datetime.today(), currency=self.currency_eur
            ).count()
            == 0
        )
