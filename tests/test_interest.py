from math import exp
import pytest
from life_contingencies import interest


# Periodic Interest Rate
def test_periodic_interest_rate_at_zero_interest():
    assert interest.periodic_interest_rate(0, 12) == 0


def test_periodic_interest_rate_reproduces_annual_accumulation():
    annual_interest_rate = 0.25
    frequency = 12
    periodic_rate = interest.periodic_interest_rate(
        annual_interest_rate,
        frequency
    )

    assert (periodic_rate + 1) ** frequency - 1 == pytest.approx(
        annual_interest_rate
    )


# Nominal Interest Rate
def test_nominal_interest_rate_at_zero_interest():
    assert interest.nominal_interest_rate(0, 12) == 0


def test_nominal_interest_rate_reproduces_annual_accumulation():
    annual_interest_rate = 0.255
    frequency = 12
    nominal_rate = interest.nominal_interest_rate(
        annual_interest_rate,
        frequency
    )

    assert (1 + nominal_rate / frequency) ** frequency - 1 == pytest.approx(
        annual_interest_rate
    )


# Discount Factor
def test_discount_factor_at_zero_interest():
    assert interest.discount_factor(0) == 1


# Effective Discount Rate
def test_effective_discount_rate_at_zero_interest():
    assert interest.effective_discount_rate(0) == 0


# Periodic Discount Rate
def test_periodic_discount_rate_at_zero_interest():
    assert interest.periodic_discount_rate(0, 12) == 0


def test_periodic_discount_rate_reproduces_annual_discount_factor():
    annual_interest_rate = 0.067
    frequency = 12
    discount_factor = 1 / (1 + annual_interest_rate)
    periodic_rate = interest.periodic_discount_rate(
        annual_interest_rate,
        frequency
    )

    assert (1 - periodic_rate) ** frequency == pytest.approx(
        discount_factor
    )


# Nominal Discount Rate
def test_nominal_discount_rate_at_zero_interest():
    assert interest.nominal_discount_rate(0, 12) == 0


def test_nominal_discount_rate_reproduces_annual_discount_factor():
    annual_interest_rate = 0.06
    frequency = 12
    discount_factor = 1 / (1 + annual_interest_rate)
    nominal_rate = interest.nominal_discount_rate(
        annual_interest_rate,
        frequency
    )

    assert (1 - nominal_rate / frequency) ** frequency == pytest.approx(
        discount_factor
    )


# Force of Interest
def test_force_of_interest_at_zero_interest():
    assert interest.force_of_interest(0) == 0


def test_force_of_interest_reproduces_annual_accumulation():
    annual_interest_rate = 0.04
    force = interest.force_of_interest(annual_interest_rate)

    assert exp(force) - 1 == pytest.approx(annual_interest_rate)
