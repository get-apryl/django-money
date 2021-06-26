import django.contrib.admin.utils as admin_utils
import pytest

from djmoney.money import Money
from .testapp.models import ModelWithVanillaMoneyField

MONEY_FIELD = ModelWithVanillaMoneyField._meta.get_field("money")
INTEGER_FIELD = ModelWithVanillaMoneyField._meta.get_field("integer")

# Babel favours the reader not the origin. If you can't read Chinese, why would
# a currency name / symbol be shown in Chinese? So these issues all regressed,
# but should be considered the better solution.
# Tests have been added to illustrate the formatting in a native locale of the
# currency.
@pytest.mark.parametrize(
    "value, locale, expected",
    (
        (Money(10, "RUB"), None, "RUB10.00"),  # Issue 232
        (Money(1234), None, "€1,234.00"),  # Issue 220
        (Money(1000, "SAR"), None, "SAR1,000.00"),  # Issue 196
        (Money(1000, "PLN"), None, "PLN1,000.00"),  # Issue 102
        (Money("3.33", "EUR"), None, "€3.33"),  # Issue 90
        (Money(10, "RUB"), "ru_RU", "10,00\xa0₽"),
        (Money(1000, "SAR"), "ar_SA", "ر.س.\u200f\xa01,000.00"),
        (Money(1000, "PLN"), "pl_PL", "1\xa0000,00\xa0zł"),
        # Eurozone
        (Money("3.33", "EUR"), "de_AT", "€\xa03,33"),
        (Money("3.33", "EUR"), "nl_BE", "€\xa03,33"),
        (Money("3.33", "EUR"), "el_CY", "3,33\xa0€"),
        (Money("3.33", "EUR"), "et_EE", "3,33\xa0€"),
        (Money("3.33", "EUR"), "fi_FI", "3,33\xa0€"),
        (Money("3.33", "EUR"), "fr_FR", "3,33\xa0€"),
        (Money("3.33", "EUR"), "de_DE", "3,33\xa0€"),
        (Money("3.33", "EUR"), "el_GR", "3,33\xa0€"),
        (Money("3.33", "EUR"), "ga_IE", "€3.33"),
        (Money("3.33", "EUR"), "it_IT", "3,33\xa0€"),
        (Money("3.33", "EUR"), "lv_LV", "3,33\xa0€"),
        (Money("3.33", "EUR"), "lt_LT", "3,33\xa0€"),
        (Money("3.33", "EUR"), "lb_LU", "3,33\xa0€"),
        (Money("3.33", "EUR"), "mt_MT", "€3.33"),
        (Money("3.33", "EUR"), "nl_NL", "€\xa03,33"),
        (Money("3.33", "EUR"), "pt_PT", "3,33\xa0€"),
        (Money("3.33", "EUR"), "sk_SK", "3,33\xa0€"),
        (Money("3.33", "EUR"), "sl_SI", "3,33\xa0€"),
        (Money("3.33", "EUR"), "es_ES", "3,33\xa0€"),
    ),
)
def test_display_for_field(settings, value, locale, expected):
    settings.USE_L10N = True
    if locale:
        settings.LANGUAGE_CODE = locale
    assert admin_utils.display_for_field(value, MONEY_FIELD, "") == expected


def test_default_display():
    assert admin_utils.display_for_field(10, INTEGER_FIELD, "") == "10"
