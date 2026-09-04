import pandas as pd


def pure_endowment(
    current_age: int,
    term: int,
    commutation_table: pd.DataFrame,
) -> float:
    if current_age not in commutation_table.index:
        raise ValueError(
            "current_age must be a valid age in the commutation table."
        )
    current_Dx = commutation_table.loc[current_age, "Dx"]

    if term < 0:
        raise ValueError("term must be a non-negative integer.")

    terminal_age = current_age + term
    omega = commutation_table.index[-1] + 1
    if terminal_age > omega:
        raise ValueError(
            "Terminal age cannot exceed the limiting age."
        )

    if terminal_age == omega:
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
    omega = commutation_table.index[-1] + 1

    # current_age validation
    if current_age not in commutation_table.index:
        raise ValueError(
            "Current age must be lower than the mortality model's "
            "terminal age."
        )
    current_Dx = commutation_table.loc[current_age, "Dx"]

    # deferral_period validation
    if deferral_period < 0:
        raise ValueError(
            "Deferral period must be a non-negative integer."
        )

    # deferred_age validation
    deferred_age = current_age + deferral_period
    if deferred_age >= omega:
        raise ValueError(
            "Deferred age cannot exceed the mortality model's "
            "terminal age."
        )
    deferred_Nx = commutation_table.loc[deferred_age, "Nx"]

    if payment_term is None:
        terminal_Nx = 0
    else:
        # payment_term validation
        if payment_term <= 0:
            raise ValueError(
                "Payment term must be a positive integer."
            )

        # terminal age validation
        terminal_age = deferred_age + payment_term
        if terminal_age > omega:
            raise ValueError(
                "Terminal age cannot exceed the mortality model's "
                "terminal age."
            )

        if terminal_age == omega:
            terminal_Nx = 0
        else:
            terminal_Nx = commutation_table.loc[terminal_age, "Nx"]

    return float((deferred_Nx - terminal_Nx) / current_Dx)


def life_annuity_immediate(
    current_age: int,
    payment_term: int,
    commutation_table: pd.DataFrame,
    deferral_period: int = 0,
) -> float:
    omega = commutation_table.index[-1] + 1

    # current_age validation
    if current_age not in commutation_table.index:
        raise ValueError(
            "Current age must be lower than the mortality model's "
            "terminal age."
        )
    current_Dx = commutation_table.loc[current_age, "Dx"]

    # deferral_period validation
    if deferral_period < 0:
        raise ValueError(
            "Deferral period must be a non-negative integer."
        )

    # deferred_age validation
    deferred_age = current_age + deferral_period + 1
    if deferred_age >= omega:
        raise ValueError(
            "Deferred age cannot exceed the mortality model's "
            "terminal age."
        )
    deferred_Nx = commutation_table.loc[deferred_age, "Nx"]

    if payment_term is None:
        terminal_Nx = 0
    else:
        # payment_term validation
        if payment_term <= 0:
            raise ValueError(
                "Payment term must be a positive integer."
            )

        # terminal age validation
        terminal_age = current_age + deferral_period + payment_term + 1
        if terminal_age > omega:
            raise ValueError(
                "Terminal age cannot exceed the mortality model's "
                "terminal age."
            )

        if terminal_age == omega:
            terminal_Nx = 0
        else:
            terminal_Nx = commutation_table.loc[terminal_age, "Nx"]

    return float((deferred_Nx - terminal_Nx) / current_Dx)


def term_life_insurance(
    current_age: int,
    term: int | None,
    commutation_table: pd.DataFrame,
    deferral_period: int = 0,
) -> float:
    omega = commutation_table.index[-1] + 1

    # current_age validation
    if current_age not in commutation_table.index:
        raise ValueError(
            "Current age must be lower than the mortality model's "
            "terminal age."
        )
    current_Dx = commutation_table.loc[current_age, 'Dx']

    # deferral_period validation
    if deferral_period < 0:
        raise ValueError(
            "Deferral period must be a non-negative integer."
        )

    # deferred_age validation
    deferred_age = current_age + deferral_period
    if deferred_age >= omega:
        raise ValueError(
            "Deferred age cannot exceed the mortality model's "
            "terminal age."
        )
    deferred_Mx = commutation_table.loc[deferred_age, 'Mx']
    
    if term in None:
        terminal_Mx = 0
    else:
        # term validation
        if term <= 0:
            raise ValueError(
                "Payment term must be a positive integer."
            )
        
        # terminal age validation
        terminal_age = deferred_age + term
        if terminal_age > omega:
                    raise ValueError(
                        "Terminal age cannot exceed the mortality model's "
                        "terminal age."
                    )
        
        if terminal_age == omega:
            terminal_Mx = 0
        else:
            terminal_Mx = commutation_table.loc[terminal_age, 'Mx']
            
    return float((deferred_Mx - terminal_Mx) / current_Dx)
