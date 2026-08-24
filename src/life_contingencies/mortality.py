import pandas as pd

def load_mortality_table(data_path):
    mortality_table = pd.read_csv(data_path, index_col=0)
    mortality_table.columns = mortality_table.columns.str.strip()
    mortality_table.index = mortality_table.index.astype(int)
        
    return mortality_table

def build_life_table(mortality_table):
    # life table - x, qx, px, lx, dx
    life_table = mortality_table.copy()

    # probability of survival - px
    life_table.loc[:,'px'] = 1 - life_table.loc[:,'qx']
    
    # survivors at age x - lx
    l0 = 10_000_000
    life_table.loc[0, 'lx'] = l0
    for x in life_table.index[1:]:
        life_table.loc[x, 'lx'] = life_table.loc[x-1,'lx'] * \
            life_table.loc[x-1, 'px']
                
    # deaths between ages x and x+1 - dx
    life_table.loc[:,'dx'] = life_table.loc[:, 'lx'] * life_table.loc[:, 'qx']
    
    return life_table