import pytest
from unittest.mock import patch

from users.factories import UserFactory
from users.models import send_welcome_email


@pytest.mark.django_db
class TestUserModel:
    @pytest.fixture(autouse=True)
    def set_up(self) -> None:
        self.user = UserFactory.create()

    def test_returns_full_name(self):
        assert (
            self.user.get_full_name() == f"{self.user.first_name} {self.user.last_name}"
        )

    def test_returns_short_name(self):
        assert self.user.get_short_name() == self.user.email

    @patch("users.models.send_mail")
    def test_returns_sent_email(self, send_mail_mock):
        subject = "Test temat"
        content = "Test zawartość"
        self.user.send_email(subject, content)

        send_mail_mock.assert_called_once()


@pytest.mark.django_db
class TestSendWelcomeEmail:
    @pytest.fixture(autouse=True)
    def set_up(self):
        self.user = UserFactory()

    @patch("users.models.User.send_email")
    def test_send_welcome_mail_when_user_is_created(self, send_email_mock):
        send_welcome_email(None, self.user, created=True)

        send_email_mock.assert_called_once()

    @patch("users.models.User.send_email")
    def test_not_send_welcome_mail_when_user_is_not_created(self, send_mail_mock):
        send_welcome_email(None, self.user, created=False)

        send_mail_mock.assert_not_called()