"""
Functions for valuing life-contingent benefits using commutation functions.
"""
import pandas as pd


def _validate_integer_params(**params):
    """Validate that the provided parameters are integers.

    Parameters
    ----------
    **params : int
        Named parameters whose values must be integers.

    Raises
    ------
    TypeError
        If any provided parameter is not an integer.
    """
    for name, value in params.items():
        if type(value) is not int:
            display_name = name.replace("_", " ").capitalize()
            raise TypeError(f"{display_name} must be an integer.")


def _validate_current_age(
    current_age: int,
    commutation_table: pd.DataFrame,
) -> None:
    """Validate that the current age exists in the commutation table.

    Parameters
    ----------
    current_age : int
        Current age of the insured.
    commutation_table : pandas.DataFrame
        Commutation table indexed by age.

    Raises
    ------
    ValueError
        If ``current_age`` is not present in the commutation table index.
    """
    if current_age not in commutation_table.index:
        raise ValueError(
            "Current age must be a valid age in the commutation table."
        )


def _get_valid_start_age(
    current_age: int,
    deferral_period: int,
    limiting_age: int,
) -> int:
    """Calculate and validate the benefit start age.

    Parameters
    ----------
    current_age : int
        Current age of the insured.
    deferral_period : int
        Number of years before the benefit or payment period begins.
    limiting_age : int
        Limiting age of the mortality model.

    Returns
    -------
    int
        Age at which the benefit or payment period begins.

    Raises
    ------
    ValueError
        If ``deferral_period`` is negative or ``start_age`` is not lower
        than ``limiting_age``.
    """
    if deferral_period < 0:
        raise ValueError(
            "Deferral period must be a non-negative integer."
        )

    start_age = current_age + deferral_period

    if start_age >= limiting_age:
        raise ValueError(
            "Start age must be lower than the limiting age."
        )

    return start_age


def pure_endowment(
    current_age: int,
    term: int,
    commutation_table: pd.DataFrame,
) -> float:
    """Calculate the actuarial present value of a pure endowment.

    Parameters
    ----------
    current_age : int
        Current age of the insured.
    term : int
        Number of years until the benefit is payable. Must be
        non-negative.
    commutation_table : pandas.DataFrame
        Commutation table indexed by age and containing a ``Dx`` column.

    Returns
    -------
    float
        Actuarial present value of a unit benefit payable at the end of
        ``term`` years if the insured survives to that time.

    Raises
    ------
    TypeError
        If ``current_age`` or ``term`` is not an integer.
    ValueError
        If ``current_age`` is not valid, ``term`` is negative, or the
        end age exceeds the limiting age.
    """
    _validate_integer_params(current_age=current_age, term=term)

    _validate_current_age(current_age, commutation_table)
    current_Dx = commutation_table.loc[current_age, "Dx"]

    if term < 0:
        raise ValueError("Term must be a non-negative integer.")

    maturity_age = current_age + term

    # The limiting age is one year beyond the last age in the table.
    limiting_age = commutation_table.index[-1] + 1
    if maturity_age > limiting_age:
        raise ValueError(
            "Maturity age cannot exceed the limiting age."
        )

    # Commutation values are zero at the limiting age.
    if maturity_age == limiting_age:
        end_Dx = 0
    else:
        end_Dx = commutation_table.loc[maturity_age, "Dx"]

    return float(end_Dx / current_Dx)


def life_annuity_due(
    current_age: int,
    payment_term: int | None,
    commutation_table: pd.DataFrame,
    deferral_period: int = 0,
) -> float:
    """Calculate the actuarial present value of a life annuity-due.

    Parameters
    ----------
    current_age : int
        Current age of the insured.
    payment_term : int or None
        Number of years for which payments are made. Must be positive
        when provided. If ``None``, payments continue for the remaining 
        lifetime of the insured.
    commutation_table : pandas.DataFrame
        Commutation table indexed by age and containing ``Dx`` and ``Nx``
        columns.
    deferral_period : int, default=0
        Number of years before payments begin. Must be non-negative.

    Returns
    -------
    float
        Actuarial present value of unit annual payments made at the
        beginning of each payment period while the insured is alive.

    Raises
    ------
    TypeError
        If an integer parameter has an invalid type.
    ValueError
        If an age, payment term, or deferral period is outside its valid
        range.
    """
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
    start_Nx = commutation_table.loc[annuity_start_age, "Nx"]

    if payment_term is None:
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
            end_Nx = 0
        else:
            end_Nx = commutation_table.loc[annuity_end_age, "Nx"]

    return float((start_Nx - end_Nx) / current_Dx)


def life_annuity_immediate(
    current_age: int,
    payment_term: int | None,
    commutation_table: pd.DataFrame,
    deferral_period: int = 0,
) -> float:
    """Calculate the actuarial present value of a life annuity-immediate.

    Parameters
    ----------
    current_age : int
        Current age of the insured.
    payment_term : int or None
        Number of years for which payments are made. Must be positive
        when provided. If ``None``, payments continue for the remaining
        lifetime of the insured.
    commutation_table : pandas.DataFrame
        Commutation table indexed by age and containing ``Dx`` and ``Nx``
        columns.
    deferral_period : int, default=0
        Number of years before the payment period begins. Must be
        non-negative.

    Returns
    -------
    float
        Actuarial present value of unit annual payments made at the end
        of each payment period while the insured is alive.

    Raises
    ------
    TypeError
        If an integer parameter has an invalid type.
    ValueError
        If an age, payment term, or deferral period is outside its valid
        range.
    """
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

    # Annuity-immediate payments occur at the end of each period,
    # so Nx is evaluated one age later.
    start_Nx_age = annuity_start_age + 1
    if start_Nx_age >= limiting_age:
        start_Nx = 0
    else:
        start_Nx = commutation_table.loc[start_Nx_age, "Nx"]

    if payment_term is None:
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

        # Commutation values are zero at and beyond the limiting age.
        end_Nx_age = annuity_end_age + 1
        if end_Nx_age >= limiting_age:
            end_Nx = 0
        else:
            end_Nx = commutation_table.loc[end_Nx_age, "Nx"]

    return float((start_Nx - end_Nx) / current_Dx)


def term_life_insurance(
    current_age: int,
    term: int,
    commutation_table: pd.DataFrame,
    deferral_period: int = 0,
) -> float:
    """Calculate the actuarial present value of term life insurance.

    Parameters
    ----------
    current_age : int
        Current age of the insured.
    term : int
        Number of years for which coverage remains in force. Must be
        positive.
    commutation_table : pandas.DataFrame
        Commutation table indexed by age and containing ``Dx`` and ``Mx``
        columns.
    deferral_period : int, default=0
        Number of years before coverage begins. Must be non-negative.

    Returns
    -------
    float
        Actuarial present value of a unit death benefit payable at the
        end of the year of death during the coverage period.

    Raises
    ------
    TypeError
        If an integer parameter has an invalid type.
    ValueError
        If an age, term, or deferral period is outside its valid range.
    """
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
        end_Mx = 0
    else:
        end_Mx = commutation_table.loc[coverage_end_age, "Mx"]

    return float((start_Mx - end_Mx) / current_Dx)


def whole_life_insurance(
    current_age: int,
    commutation_table: pd.DataFrame,
    deferral_period: int = 0,
) -> float:
    """Calculate the actuarial present value of whole life insurance.

    Parameters
    ----------
    current_age : int
        Current age of the insured.
    commutation_table : pandas.DataFrame
        Commutation table indexed by age and containing ``Dx`` and ``Mx``
        columns.
    deferral_period : int, default=0
        Number of years before coverage begins. Must be non-negative.

    Returns
    -------
    float
        Actuarial present value of a unit death benefit payable at the
        end of the year of death, with coverage continuing for the
        remaining lifetime of the insured.

    Raises
    ------
    TypeError
        If an integer parameter has an invalid type.
    ValueError
        If ``current_age`` or the deferred age is outside its valid range,
        or if ``deferral_period`` is negative.
    """
    _validate_integer_params(
        current_age=current_age,
        deferral_period=deferral_period,
    )

    # The limiting age is one year beyond the last table age.
    limiting_age = commutation_table.index[-1] + 1

    _validate_current_age(current_age, commutation_table)
    current_Dx = commutation_table.loc[current_age, "Dx"]

    coverage_start_age = _get_valid_start_age(
            current_age,
            deferral_period,
            limiting_age,
    )
    start_Mx = commutation_table.loc[coverage_start_age, "Mx"]

    return float(start_Mx / current_Dx)
