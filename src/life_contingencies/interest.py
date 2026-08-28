import math


def periodic_interest_rate(
    interest_rate: float,
    frequency: int,
) -> float:
    """Calculate the equivalent effective interest rate per compounding
    period.

    Parameters
    ----------
    interest_rate : float
        Annual effective interest rate. Must be non-negative.
    frequency : int
        Number of compounding periods per year. Must be a positive
        integer.

    Returns
    -------
    float
        Equivalent effective interest rate per compounding period.
    """
    periodic_rate = (1 + interest_rate) ** (1 / frequency) - 1

    return periodic_rate


def nominal_interest_rate(
    interest_rate: float,
    frequency: int,
) -> float:
    """Calculate the equivalent nominal annual interest rate.

    Parameters
    ----------
    interest_rate : float
        Annual effective interest rate. Must be non-negative.
    frequency : int
        Number of compounding periods per year. Must be a positive
        integer.

    Returns
    -------
    float
        Equivalent nominal annual interest rate convertible at the
    specified frequency.
    """
    periodic_rate = periodic_interest_rate(interest_rate, frequency)
    nominal_rate = periodic_rate * frequency

    return nominal_rate


def discount_factor(interest_rate: float) -> float:
    """Calculate the discount factor for an effective interest rate.

    Parameters
    ----------
    interest_rate : float
        Effective interest rate for the corresponding period.
        Must be non-negative.

    Returns
    -------
    float
        Discount factor corresponding to the effective interest rate.
    """
    return 1 / (1 + interest_rate)


def effective_discount_rate(interest_rate: float) -> float:
    """Calculate the effective discount rate.

    Parameters
    ----------
    interest_rate : float
        Effective interest rate for the corresponding period.
        Must be non-negative.

    Returns
    -------
    float
        Equivalent effective discount rate for the same period.
    """
    v = discount_factor(interest_rate)
    discount_rate = 1 - v

    return discount_rate


def periodic_discount_rate(
    interest_rate: float,
    frequency: int,
) -> float:
    """Calculate the equivalent effective discount rate per period.

    Parameters
    ----------
    interest_rate : float
        Annual effective interest rate. Must be non-negative.
    frequency : int
        Number of periods per year. Must be a positive integer.

    Returns
    -------
    float
        Equivalent effective discount rate per period.
    """
    v = discount_factor(interest_rate)
    periodic_discount = 1 - v ** (1 / frequency)

    return periodic_discount


def nominal_discount_rate(
    interest_rate: float,
    frequency: int,
) -> float:
    """Calculate the equivalent nominal annual discount rate.

    Parameters
    ----------
    interest_rate : float
        Annual effective interest rate. Must be non-negative.
    frequency : int
        Number of conversion periods per year. Must be a positive
        integer.

    Returns
    -------
    float
        Equivalent nominal annual discount rate convertible at the
        specified frequency.
    """
    periodic_discount = periodic_discount_rate(interest_rate, frequency)
    nominal_discount = periodic_discount * frequency

    return nominal_discount


def force_of_interest(interest_rate: float) -> float:
    """Calculate the equivalent force of interest.

    Parameters
    ----------
    interest_rate : float
        Annual effective interest rate. Must be non-negative.

    Returns
    -------
    float
        Equivalent force of interest.
    """
    return math.log(1 + interest_rate)
