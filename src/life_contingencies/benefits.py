import pandas as pd


def pure_endowment(
    current_age: int,
    term: int,
    commutation_table: pd.DataFrame,
) -> float:
    if current_age not in commutation_table.index:
        raise ValueError(
            "Current age must be a valid age in the commutation table."
        )
    current_Dx = commutation_table.loc[current_age, "Dx"]

    if term < 0:
        raise ValueError("Term must be a non-negative integer.")

    terminal_age = current_age + term
    # The limiting age is one year beyond the last age in the table.
    omega = commutation_table.index[-1] + 1
    if terminal_age > omega:
        raise ValueError(
            "Terminal age cannot exceed the limiting age."
        )

    if terminal_age == omega:
        # Commutation values are zero at the limiting age.
        terminal_Dx = 0
    else:
        terminal_Dx = commutation_table.loc[current_age + term, "Dx"]

    return float(terminal_Dx / current_Dx)


def life_annuity_due(
    current_age: int,
    payment_term: int | None,
    commutation_table: pd.DataFrame,
    deferral_period: int = 0,
) -> float:
    # The limiting age is one year beyond the last age in the table.
    omega = commutation_table.index[-1] + 1

    if current_age not in commutation_table.index:
        raise ValueError(
            "Current age must be a valid age in the commutation table."
        )
    current_Dx = commutation_table.loc[current_age, "Dx"]

    if deferral_period < 0:
        raise ValueError(
            "Deferral period must be a non-negative integer."
        )

    deferred_age = current_age + deferral_period
    if deferred_age >= omega:
        raise ValueError(
            "Deferred age must be lower than the limiting age."
        )
    deferred_Nx = commutation_table.loc[deferred_age, "Nx"]

    if payment_term is None:
        terminal_Nx = 0
    else:
        if payment_term <= 0:
            raise ValueError(
                "Payment term must be a positive integer."
            )

        terminal_age = deferred_age + payment_term
        if terminal_age > omega:
            raise ValueError(
                "Terminal age cannot exceed the limiting age."
            )

        if terminal_age == omega:
            # Commutation values are zero at the limiting age.
            terminal_Nx = 0
        else:
            terminal_Nx = commutation_table.loc[terminal_age, "Nx"]

    return float((deferred_Nx - terminal_Nx) / current_Dx)


def life_annuity_immediate(
    current_age: int,
    payment_term: int | None,
    commutation_table: pd.DataFrame,
    deferral_period: int = 0,
) -> float:
    # The limiting age is one year beyond the last age in the table.
    omega = commutation_table.index[-1] + 1

    if current_age not in commutation_table.index:
        raise ValueError(
            "Current age must be a valid age in the commutation table."
        )
    current_Dx = commutation_table.loc[current_age, "Dx"]

    if deferral_period < 0:
        raise ValueError(
            "Deferral period must be a non-negative integer."
        )

    deferred_age = current_age + deferral_period
    if deferred_age >= omega:
        raise ValueError(
            "Deferred age must be lower than the limiting age."
        )

    # Annuity-immediate payments occur at the end of each period,
    # so Nx is evaluated one age later.
    deferred_Nx_age = deferred_age + 1
    if deferred_Nx_age >= omega:
        deferred_Nx = 0
    else:
        deferred_Nx = commutation_table.loc[deferred_Nx_age, "Nx"]

    if payment_term is None:
        terminal_Nx = 0
    else:
        if payment_term <= 0:
            raise ValueError(
                "Payment term must be a positive integer."
            )

        terminal_age = deferred_age + payment_term
        if terminal_age > omega:
            raise ValueError(
                "Terminal age cannot exceed the limiting age."
            )

        # Commutation values are zero at and beyond the limiting age.
        terminal_Nx_age = terminal_age + 1
        if terminal_Nx_age >= omega:
            terminal_Nx = 0
        else:
            terminal_Nx = commutation_table.loc[terminal_Nx_age, "Nx"]

    return float((deferred_Nx - terminal_Nx) / current_Dx)


def term_life_insurance(
    current_age: int,
    term: int | None,
    commutation_table: pd.DataFrame,
    deferral_period: int = 0,
) -> float:
    # The limiting age is one year beyond the last age in the table.
    omega = commutation_table.index[-1] + 1

    if current_age not in commutation_table.index:
        raise ValueError(
            "Current age must be a valid age in the commutation table."
        )
    current_Dx = commutation_table.loc[current_age, "Dx"]

    if deferral_period < 0:
        raise ValueError(
            "Deferral period must be a non-negative integer."
        )

    deferred_age = current_age + deferral_period
    if deferred_age >= omega:
        raise ValueError(
            "Deferred age must be lower than the limiting age."
        )
    deferred_Mx = commutation_table.loc[deferred_age, "Mx"]

    if term is None:
        terminal_Mx = 0
    else:
        if term <= 0:
            raise ValueError(
                "Term must be a positive integer."
            )

        terminal_age = deferred_age + term
        if terminal_age > omega:
            raise ValueError(
                "Terminal age cannot exceed the limiting age."
            )

        if terminal_age == omega:
            # Commutation values are zero at the limiting age.
            terminal_Mx = 0
        else:
            terminal_Mx = commutation_table.loc[terminal_age, "Mx"]

    return float((deferred_Mx - terminal_Mx) / current_Dx)
