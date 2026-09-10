import pytest
from life_contingencies import interest

def test_periodic_interest_rate_zero_interest():
    
    assert interest.periodic_interest_rate(0, 12) == 0


def test_nominal_interest_rate_zero_interest():
    
    assert interest.nominal_interest_rate(0, 12) == 0


def test_discount_factor_zero_interest():
    
    assert interest.discount_factor(0) == 1


def test_effective_discount_rate_zero_interest():
    
    assert interest.effective_discount_rate(0) == 0


def test_periodic_discount_rate_zero_interest():
    
    assert interest.periodic_discount_rate(0, 12) == 0


def test_nominal_discount_rate_zero_interest():
    
    assert interest.nominal_discount_rate(0, 12) == 0


def test_force_of_interest_zero_interest():
    
    assert interest.force_of_interest(0) == 0