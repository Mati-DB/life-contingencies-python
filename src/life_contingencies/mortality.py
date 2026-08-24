import pandas as pd


def load_mortality_table(data_path):
    """Load a mortality table from a CSV file and normalize its 
    structure.

    Parameters
    ----------
    data_path : pathlib.Path
        Path to the mortality table CSV file.

    Returns
    -------
    pandas.DataFrame
        Mortality table indexed by integer ages with normalized column 
        names.
    """
    mortality_table = pd.read_csv(data_path, index_col=0)
    mortality_table.columns = mortality_table.columns.str.strip()
    mortality_table.index = mortality_table.index.astype(int)
        
    return mortality_table


def build_life_table(mortality_table, radix=10_000_000):
    """Build a life table from mortality probabilities.

    Parameters
    ----------
    mortality_table : pandas.DataFrame
        Mortality table indexed by age and containing a ``qx`` column.
    radix : int, default=10_000_000
        Initial number of lives at age 0.

    Returns
    -------
    pandas.DataFrame
        Life table with the following columns:

        - ``qx``: probability of death between ages x and x + 1.
        - ``px``: probability of survival from age x to age x + 1.
        - ``lx``: number of lives surviving to exact age x.
        - ``dx``: number of deaths between ages x and x + 1.
    """

    life_table = mortality_table.copy()
    life_table.loc[:, 'px'] = 1 - life_table.loc[:, 'qx']
    life_table.loc[0, 'lx'] = radix
    
    for x in life_table.index[1:]:
        life_table.loc[x, 'lx'] = (
            life_table.loc[x - 1, 'lx'] * life_table.loc[x - 1, 'px']
        )
    life_table.loc[:, 'dx'] = life_table.loc[:, 'lx'] * life_table.loc[:, 'qx']
    
    return life_table

