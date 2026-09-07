"""
This module provides functions for interest rate equivalence
calculations.
"""
import math
from numbers import Real
from ._validation import _validate_integer_params


def _validate_non_negativity(**params):
    """Validate that the provided parameters are non-negative.

    Parameters
    ----------
    **params : Real
        Named numeric parameters whose values must be non-negative.

    Raises
    ------
    ValueError
        If any provided parameter is negative.
    """
    for name, value in params.items():
            if value < 0:
                display_name = name.replace("_", " ").capitalize()
                raise ValueError(f"{display_name} must be non-negative.")


def _validate_numeric(**params):
    """Validate that the provided parameters are numeric values.

    Parameters
    ----------
    **params : Real
        Named parameters whose values must be real numbers.

    Raises
    ------
    TypeError
        If any provided parameter is not real number.
    """
    for name, value in params.items():
        if not isinstance(value, Real):
            display_name = name.replace("_", " ").capitalize()
            raise TypeError(f"{display_name} must be a real number.")


def _validate_positivity(**params):
    """Validate that the provided parameters are positive.

    Parameters
    ----------
    **params : Real
        Named numeric parameters whose values must be greater than zero.

    Raises
    ------
    ValueError
        If any provided parameter is not greater than zero.
    """
    for name, value in params.items():
            if value <= 0:
                display_name = name.replace("_", " ").capitalize()
                raise ValueError(f"{display_name} must be greater than zero.")


def periodic_interest_rate(
    interest_rate: Real,
    frequency: int,
) -> Real:
    """Calculate the equivalent effective interest rate per compounding
    period.

    Parameters
    ----------
    interest_rate : number.Real
        Annual effective interest rate. Must be a real non-negative
        number.
    frequency : int
        Number of compounding periods per year. Must be a positive
        integer.

    Returns
    -------
    number.Real
        Equivalent effective interest rate per compounding period.
    """
    _validate_integer_params(frequency=frequency)
    _validate_positivity(frequency=frequency)

    _validate_numeric(interest_rate=interest_rate)
    _validate_non_negativity(interest_rate=interest_rate)
    
    periodic_rate = (1 + interest_rate) ** (1 / frequency) - 1

    return periodic_rate


def nominal_interest_rate(
    interest_rate: Real,
    frequency: int,
) -> Real:
    """Calculate the equivalent nominal annual interest rate.

    Parameters
    ----------
    interest_rate : number.Real
        Annual effective interest rate. Must be a real non-negative
        number.
    frequency : int
        Number of compounding periods per year. Must be a positive
        integer.

    Returns
    -------
    number.Real
        Equivalent nominal annual interest rate convertible at the
    specified frequency.
    """
    _validate_integer_params(frequency=frequency)
    _validate_positivity(frequency=frequency)

    _validate_numeric(interest_rate=interest_rate)
    _validate_non_negativity(interest_rate=interest_rate)
 
    periodic_rate = periodic_interest_rate(interest_rate, frequency)
    nominal_rate = periodic_rate * frequency

    return nominal_rate


def discount_factor(interest_rate: Real) -> Real:
    """Calculate the discount factor for an effective interest rate.

    Parameters
    ----------
    interest_rate : number.Real
        Effective interest rate for the corresponding period.
        Must be a real non-negative number.

    Returns
    -------
    number.Real
        Discount factor corresponding to the effective interest rate.
    """
    _validate_numeric(interest_rate=interest_rate)
    _validate_non_negativity(interest_rate=interest_rate)
 
    return 1 / (1 + interest_rate)


def effective_discount_rate(interest_rate: Real) -> Real:
    """Calculate the effective discount rate.

    Parameters
    ----------
    interest_rate : number.Real
        Effective interest rate for the corresponding period.
        Must be a real non-negative number.

    Returns
    -------
    umber.Real
        Equivalent effective discount rate for the same period.
    """
    _validate_numeric(interest_rate=interest_rate)
    _validate_non_negativity(interest_rate=interest_rate)
 
    v = discount_factor(interest_rate)
    discount_rate = 1 - v

    return discount_rate


def periodic_discount_rate(
    interest_rate: Real,
    frequency: int,
) -> Real:
    """Calculate the equivalent effective discount rate per period.

    Parameters
    ----------
    interest_rate : number.Real
        Annual effective interest rate. Must be a real non-negative
        number.
    frequency : int
        Number of periods per year. Must be a positive integer.

    Returns
    -------
    number.Real
        Equivalent effective discount rate per period.
    """
    _validate_integer_params(frequency=frequency)
    _validate_positivity(frequency=frequency)

    _validate_numeric(interest_rate=interest_rate)
    _validate_non_negativity(interest_rate=interest_rate)
 
    v = discount_factor(interest_rate)
    periodic_discount = 1 - v ** (1 / frequency)

    return periodic_discount


def nominal_discount_rate(
    interest_rate: Real,
    frequency: int,
) -> Real:
    """Calculate the equivalent nominal annual discount rate.

    Parameters
    ----------
    interest_rate : number.Real
        Annual effective interest rate. Must be a real non-negative
        number.
    frequency : int
        Number of conversion periods per year. Must be a positive
        integer.

    Returns
    -------
    number.Real
        Equivalent nominal annual discount rate convertible at the
        specified frequency.
    """
    _validate_integer_params(frequency=frequency)
    _validate_positivity(frequency=frequency)

    _validate_numeric(interest_rate=interest_rate)
    _validate_non_negativity(interest_rate=interest_rate)
 
    periodic_discount = periodic_discount_rate(interest_rate, frequency)
    nominal_discount = periodic_discount * frequency

    return nominal_discount


def force_of_interest(interest_rate: Real) -> Real:
    """Calculate the equivalent force of interest.

    Parameters
    ----------
    interest_rate : number.Real
        Annual effective interest rate. Must be a real non-negative
        number.

    Returns
    -------
    number.Real
        Equivalent force of interest.
    """
    _validate_numeric(interest_rate=interest_rate)
    _validate_non_negativity(interest_rate=interest_rate)
 
    return math.log(1 + interest_rate)
