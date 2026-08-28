import pandas as pd


def pure_endowment(
    current_age: int,
    term: int,
    commutation_table: pd.DataFrame,
) -> float:
    terminal_Dx = commutation_table.loc[current_age + term, 'Dx']
    current_Dx = commutation_table.loc[current_age, 'Dx']

    return terminal_Dx / current_Dx


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

    return (deferred_Nx - terminal_Nx) / current_Dx


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

    return (deferred_Nx - terminal_Nx) / current_Dx
