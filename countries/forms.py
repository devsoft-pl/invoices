from django import forms
from django.utils.translation import gettext as _

from base.validators import country_validator
from countries.models import Country


class CountryForm(forms.ModelForm):
    next = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

        country_field: forms.CharField = self.fields["country"]
        country_field.widget.attrs["class"] = "form-control"
        country_field.validators = [country_validator]

    class Meta:
        model = Country
        fields = ["next", "country"]

    def clean_country(self):
        country = self.cleaned_data.get("country")
        land = Country.objects.filter(country=country, user=self.user)

        if land.exists():
            raise forms.ValidationError(_("Country already exists"))

        return country
