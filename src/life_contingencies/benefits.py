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
    payment_term: int,
    commutation_table: pd.DataFrame,
    deferral_period: int = 0,
) -> float:
    deferred_Nx = commutation_table.loc[current_age + deferral_period, 'Nx']
    terminal_Nx = commutation_table.loc[
        current_age + payment_term + deferral_period, 'Nx']
    current_Dx = commutation_table.loc[current_age, 'Dx']

    omega = commutation_table.index[-1]
    terminal_age = current_age + deferral_period + payment_term
    # Commutation values beyond omega are treated as zero.
    if terminal_age <= omega:
        # Terminal benefit age within table bounds
        premium = (deferred_Nx - terminal_Nx) / current_Dx
    else:
        # Terminal benefit age out of table bounds
        premium = deferred_Nx / current_Dx

    return premium


def life_annuity_immediate(
    current_age: int,
    payment_term: int,
    commutation_table: pd.DataFrame,
    deferral_period: int = 0,
) -> float:
    deferred_Nx = commutation_table.loc[
        current_age + deferral_period + 1, 'Nx']
    terminal_Nx = commutation_table.loc[
        current_age + deferral_period + payment_term + 1, 'Nx']
    current_Dx = commutation_table.loc[current_age, 'Dx']

    omega = commutation_table.index[-1]
    terminal_age = current_age + deferral_period + payment_term
    # Commutation values beyond omega are treated as zero.
    if terminal_age <= omega:
        # Terminal benefit age within table bounds
        premium = (deferred_Nx - terminal_Nx) / current_Dx
    else:
        # Terminal benefit age out of table bounds
        premium = deferred_Nx / current_Dx

    return premium


def term_life_insurance(
    current_age: int,
    term: int,
    commutation_table: pd.DataFrame,
    deferral_period: int = 0,
) -> float:
    deferred_Mx = commutation_table.loc[
        current_age + deferral_period, 'Mx']
    terminal_Mx = commutation_table.loc[
        current_age + deferral_period + term, 'Mx']
    current_Dx = commutation_table.loc[
        current_age, 'Dx']

    omega = commutation_table.index[-1]
    terminal_age = current_age + deferral_period + term
    # Commutation values beyond omega are treated as zero.
    if terminal_age <= omega:
        # Terminal benefit age within table bounds
        premium = (deferred_Mx - terminal_Mx) / current_Dx
    else:
        # Terminal benefit age out of table bounds
        premium = deferred_Mx / current_Dx

    return premium
