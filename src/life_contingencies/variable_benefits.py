"""
Functions for valuing variable life-contingent benefits using
commutation functions.
"""
import pandas as pd
from ._validation import _validate_integer_params
from .level_benefits import _get_valid_start_age, _validate_current_age


def increasing_life_annuity(
    current_age: int,
    payment_term: int | None,
    commutation_table: pd.DataFrame,
    deferral_period: int = 0,
) -> float:
    _validate_integer_params(
        current_age=current_age,
        deferral_period=deferral_period,
    )

    if payment_term is not None:
        _validate_integer_params(payment_term=payment_term)

    # The limiting age is one year beyond the last table age.
    limiting_age = commutation_table.index[-1] + 1

    _validate_current_age(current_age, commutation_table)
    current_Dx = commutation_table.loc[current_age, "Dx"]

    annuity_start_age = _get_valid_start_age(
        current_age,
        deferral_period,
        limiting_age,
    )
    start_Sx = commutation_table.loc[annuity_start_age, "Sx"]

    if payment_term is None:
        end_Sx = 0
        end_Nx = 0
    else:
        if payment_term <= 0:
            raise ValueError(
                "Payment term must be a positive integer."
            )

        annuity_end_age = annuity_start_age + payment_term
        if annuity_end_age > limiting_age:
            raise ValueError(
                "Payment end age cannot exceed the limiting age."
            )

        # Commutation values are zero at the limiting age.
        if annuity_end_age == limiting_age:
            end_Sx = 0
            end_Nx = 0
        else:
            end_Sx = commutation_table.loc[annuity_end_age, "Sx"]
            end_Nx = commutation_table.loc[annuity_end_age, "Nx"]

    return float((start_Sx - end_Sx - payment_term * end_Nx) / current_Dx)


def arithmetic_progression_life_annuity(
    current_age: int,
    payment_term: int | None,
    commutation_table: pd.DataFrame,
    increment_rate: float,
    deferral_period: int = 0,
) -> float:
    _validate_integer_params(
        current_age=current_age,
        deferral_period=deferral_period,
    )

    if payment_term is not None:
        _validate_integer_params(payment_term=payment_term)

    # The limiting age is one year beyond the last table age.
    limiting_age = commutation_table.index[-1] + 1

    _validate_current_age(current_age, commutation_table)
    current_Dx = commutation_table.loc[current_age, "Dx"]

    annuity_start_age = _get_valid_start_age(
        current_age,
        deferral_period,
        limiting_age,
    )
    start_Sx = commutation_table.loc[annuity_start_age, "Sx"]
    start_Nx = commutation_table.loc[annuity_start_age, "Nx"]

    if payment_term is None:
        end_Sx = 0
        end_Nx = 0
    else:
        if payment_term <= 0:
            raise ValueError(
                "Payment term must be a positive integer."
            )

        annuity_end_age = annuity_start_age + payment_term
        if annuity_end_age > limiting_age:
            raise ValueError(
                "Payment end age cannot exceed the limiting age."
            )

        # Commutation values are zero at the limiting age.
        if annuity_end_age == limiting_age:
            end_Sx = 0
            end_Nx = 0
        else:
            end_Sx = commutation_table.loc[annuity_end_age, "Sx"]
            end_Nx = commutation_table.loc[annuity_end_age, "Nx"]

    base_annuity = (start_Nx - end_Nx) / current_Dx
    increasing_annuity = increasing_life_annuity(
        current_age,
        payment_term - 1,
        commutation_table,
        deferral_period + 1,
    )

    return float(base_annuity + increment_rate * increasing_annuity)


def increasing_term_life_insurance(
    current_age: int,
    term: int,
    commutation_table: pd.DataFrame,
    deferral_period: int = 0,
) -> float:
    
    _validate_integer_params(
    current_age=current_age,
    term=term,
    deferral_period=deferral_period,
    )

    # Limiting age is one year beyond the last table age.
    limiting_age = commutation_table.index[-1] + 1

    _validate_current_age(current_age, commutation_table)
    current_Dx = commutation_table.loc[current_age, "Dx"]

    coverage_start_age = _get_valid_start_age(
        current_age,
        deferral_period,
        limiting_age,
    )
    start_Rx = commutation_table.loc[coverage_start_age, "Rx"]

    if term <= 0:
        raise ValueError(
            "Term must be a positive integer."
        )

    coverage_end_age  = coverage_start_age + term
    if coverage_end_age  > limiting_age:
        raise ValueError(
            "Coverage end age cannot exceed the limiting age."
        )

    # Commutation values are zero at the limiting age.
    if coverage_end_age  == limiting_age:
        end_Rx = 0
        emd_Mx = 0
    else:
        end_Rx = commutation_table.loc[coverage_end_age, "Rx"]
        end_Mx = commutation_table.loc[coverage_end_age, "Mx"]

    return float((start_Rx - end_Rx - term * end_Mx) / current_Dx)


def arithmetic_progression_life_insurance(
    current_age: int,
    term: int,
    commutation_table: pd.DataFrame,
    increment_rate: float,
    deferral_period: int = 0,
) -> float:
    
    _validate_integer_params(
    current_age=current_age,
    term=term,
    deferral_period=deferral_period,
    )

    # Limiting age is one year beyond the last table age.
    limiting_age = commutation_table.index[-1] + 1

    _validate_current_age(current_age, commutation_table)
    current_Dx = commutation_table.loc[current_age, "Dx"]

    coverage_start_age = _get_valid_start_age(
        current_age,
        deferral_period,
        limiting_age,
    )
    start_Rx = commutation_table.loc[coverage_start_age, "Rx"]
    start_Mx = commutation_table.loc[coverage_start_age, "Mx"]

    if term <= 0:
        raise ValueError(
            "Term must be a positive integer."
        )

    coverage_end_age  = coverage_start_age + term
    if coverage_end_age  > limiting_age:
        raise ValueError(
            "Coverage end age cannot exceed the limiting age."
        )

    # Commutation values are zero at the limiting age.
    if coverage_end_age  == limiting_age:
        end_Rx = 0
        emd_Mx = 0
    else:
        end_Rx = commutation_table.loc[coverage_end_age, "Rx"]
        end_Mx = commutation_table.loc[coverage_end_age, "Mx"]

    base_term_insurance = (start_Mx - end_Mx) / current_Dx
    increasing_term_insurance = increasing_term_insurance(
        current_age,
        term,
        commutation_table,
        deferral_period,
    )

    return float(
        base_term_insurance + increment_rate * increasing_term_insurance
    )
