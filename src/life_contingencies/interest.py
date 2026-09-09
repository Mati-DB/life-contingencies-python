"""Functions for interest rate equivalence calculations."""
import math
from numbers import Real
from ._validation import _validate_integer_params


def _validate_non_negativity(**params):
    """Validate that the provided parameters are non-negative.

    Parameters
    ----------
    **params : numbers.Real
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
    """Validate that the provided parameters are finite real numbers.

    Parameters
    ----------
    **params : numbers.Real
        Named parameters whose values must be finite real numbers.

    Raises
    ------
    TypeError
        If any provided parameter is not a real number.
    ValueError
        If any provided parameter is not finite.
    """
    for name, value in params.items():
        display_name = name.replace("_", " ").capitalize()

        if not isinstance(value, Real) or isinstance(value, bool):
            raise TypeError(f"{display_name} must be a real number.")

        if not math.isfinite(value):
            raise ValueError(f"{display_name} must be finite.")


def _validate_positivity(**params):
    """Validate that the provided parameters are positive.

    Parameters
    ----------
    **params : numbers.Real
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
    interest_rate : numbers.Real
        Annual effective interest rate. Must be a finite, non-negative
        real number.
    frequency : int
        Number of compounding periods per year. Must be a positive
        integer.

    Returns
    -------
    numbers.Real
        Equivalent effective interest rate per compounding period.

    Raises
    ------
    TypeError
        If ``interest_rate`` is not a real number or ``frequency`` is
        not an integer.
    ValueError
        If ``interest_rate`` is not finite or is negative, or
        ``frequency`` is not positive.
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
    interest_rate : numbers.Real
        Annual effective interest rate. Must be a finite, non-negative
        real number.
    frequency : int
        Number of compounding periods per year. Must be a positive
        integer.

    Returns
    -------
    numbers.Real
        Equivalent nominal annual interest rate convertible at the
    specified frequency.

    Raises
    ------
    TypeError
        If ``interest_rate`` is not a real number or ``frequency`` is
        not an integer.
    ValueError
        If ``interest_rate`` is not finite or is negative, or
        ``frequency`` is not positive.
    """
    periodic_rate = periodic_interest_rate(interest_rate, frequency)
    nominal_rate = periodic_rate * frequency

    return nominal_rate


def discount_factor(interest_rate: Real) -> Real:
    """Calculate the discount factor for an effective interest rate.

    Parameters
    ----------
    interest_rate : numbers.Real
        Effective interest rate for the corresponding period.
        Must be a finite, non-negative real number.

    Returns
    -------
    numbers.Real
        Discount factor corresponding to the effective interest rate.

    Raises
    ------
    TypeError
        If ``interest_rate`` is not a real number.
    ValueError
        If ``interest_rate`` is not finite or is negative.
    """
    _validate_numeric(interest_rate=interest_rate)
    _validate_non_negativity(interest_rate=interest_rate)

    return 1 / (1 + interest_rate)


def effective_discount_rate(interest_rate: Real) -> Real:
    """Calculate the effective discount rate.

    Parameters
    ----------
    interest_rate : numbers.Real
        Effective interest rate for the corresponding period. Must be a
        finite, non-negative real number.

    Returns
    -------
    numbers.Real
        Equivalent effective discount rate for the same period.

    Raises
    ------
    TypeError
        If ``interest_rate`` is not a real number.
    ValueError
        If ``interest_rate`` is not finite or is negative.
    """
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
    interest_rate : numbers.Real
        Annual effective interest rate. Must be a finite, non-negative
        real number.
    frequency : int
        Number of periods per year. Must be a positive integer.

    Returns
    -------
    numbers.Real
        Equivalent effective discount rate per period.

    Raises
    ------
    TypeError
        If ``interest_rate`` is not a real number or ``frequency`` is
        not an integer.
    ValueError
        If ``interest_rate`` is not finite or is negative, or
        ``frequency`` is not positive.
    """
    _validate_integer_params(frequency=frequency)
    _validate_positivity(frequency=frequency)

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
    interest_rate : numbers.Real
        Annual effective interest rate. Must be a finite, non-negative
        real number.
    frequency : int
        Number of conversion periods per year. Must be a positive
        integer.

    Returns
    -------
    numbers.Real
        Equivalent nominal annual discount rate convertible at the
        specified frequency.

    Raises
    ------
    TypeError
        If ``interest_rate`` is not a real number or ``frequency`` is
        not an integer.
    ValueError
        If ``interest_rate`` is not finite or is negative, or
        ``frequency`` is not positive.
    """
    periodic_discount = periodic_discount_rate(interest_rate, frequency)
    nominal_discount = periodic_discount * frequency

    return nominal_discount


def force_of_interest(interest_rate: Real) -> Real:
    """Calculate the equivalent force of interest.

    Parameters
    ----------
    interest_rate : numbers.Real
        Annual effective interest rate. Must be a finite, non-negative
        real number.

    Returns
    -------
    numbers.Real
        Equivalent force of interest.

    Raises
    ------
    TypeError
        If ``interest_rate`` is not a real number.
    ValueError
        If ``interest_rate`` is not finite or is negative.
    """
    _validate_numeric(interest_rate=interest_rate)
    _validate_non_negativity(interest_rate=interest_rate)

    return math.log(1 + interest_rate)
