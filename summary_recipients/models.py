from django.db import models
from django.utils.translation import gettext as _

from companies.models import Company
from countries.models import Country
from users.models import User


class SummaryRecipient(models.Model):
    MONTHLY = 0
    QUARTERLY = 1

    SETTLEMENT_TYPES = (
        (MONTHLY, _("Monthly")),
        (QUARTERLY, _("Quarterly")),
    )

    description = models.CharField(verbose_name=_("Description"), max_length=50)
    company = models.ForeignKey(
        Company,
        verbose_name=_("Company"),
        on_delete=models.CASCADE,
        related_name="summary_recipients",
    )
    day = models.IntegerField(verbose_name=_("Day of send"))
    email = models.EmailField(_("Email"))
    settlement_types = models.IntegerField(
        verbose_name=_("Settlement types"), choices=SETTLEMENT_TYPES
    )

    def __str__(self):
        return self.description