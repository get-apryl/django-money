import pytest
from django.utils.translation import override

from djmoney.money import DefaultMoney, Money, get_current_locale


def test_repr():
    assert repr(Money("10.5", "USD")) == "<Money: 10.5 USD>"

def test_for_eval():
    m = Money("10.5", "USD")
    assert m == eval(m.for_eval())

def test_html_safe():
    assert Money("10.5", "EUR").__html__() == u"€10.50"


def test_html_unsafe():
    class UnsafeMoney(Money):
        def __str__(self):
            return "<script>"

    assert UnsafeMoney().__html__() == "&lt;script&gt;"


def test_default_mul():
    assert Money(10, "USD") * 2 == Money(20, "USD")


def test_default_truediv():
    assert Money(10, "USD") / 2 == Money(5, "USD")
    assert Money(10, "USD") / Money(2, "USD") == 5


def test_reverse_truediv_fails():
    with pytest.raises(TypeError):
        10 / Money(5, "USD")


@pytest.mark.parametrize("locale, expected", (("pl", "PL_PL"), ("pl_PL", "pl_PL")))
def test_get_current_locale(locale, expected):
    with override(locale):
        assert get_current_locale() == expected


def test_round():
    assert round(Money("1.69", "USD"), 1) == Money("1.7", "USD")


def test_configurable_decimal_number():
    # Override default configuration per instance, keeps human readable output to default
    mny = Money("10.543", "USD", decimal_places=3)
    assert str(mny) == "$10.54"
    assert mny.decimal_places == 3


def test_add_decimal_places():
    one = Money("1.0000", "USD", decimal_places=4)
    two = Money("2.000000005", "USD", decimal_places=10)

    result = one + two
    assert result.decimal_places == 10


def test_add_decimal_places_zero():
    two = Money("2.005", "USD", decimal_places=3)

    result = two + 0
    assert result.decimal_places == 3


def test_sub_negative():
    # See GH-593
    total = DefaultMoney(0, "EUR")
    bills = (Money(8, "EUR"), Money(25, "EUR"))
    for bill in bills:
        total -= bill
    assert total == Money(-33, "EUR")
