import math


def periodic_interest_rate(
    interest_rate: float,
    frequency: int,
) -> float:
    periodic_rate = (1 + interest_rate) ** (1 / frequency) - 1

    return periodic_rate


def nominal_interest_rate(
    interest_rate: float,
    frequency: int
) -> float:
    periodic_rate = periodic_interest_rate(interest_rate, frequency)
    nominal_rate = periodic_rate * frequency

    return nominal_rate


def discount_factor(interest_rate: float) -> float:
    return 1 / (1 + interest_rate)


def effective_discount_rate(interest_rate: float) -> float:
    v = discount_factor(interest_rate)
    discount_rate = 1 - v

    return discount_rate


def periodic_discount_rate(
    interest_rate: float,
    frequency: int
) -> float:
    v = discount_factor(interest_rate)
    periodic_discount = 1 - v ** (1 / frequency)

    return periodic_discount


def nominal_discount_rate(
    interest_rate: float,
    frequency: int
) -> float:
    periodic_discount = periodic_discount_rate(interest_rate, frequency)
    nominal_discount = periodic_discount * frequency

    return nominal_discount


def force_of_interest(interest_rate: float) -> float:
    return math.log(1 + interest_rate)
