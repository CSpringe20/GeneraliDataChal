import pandas as pd
from enginee import recommend_coverages

import numpy as np

def engine(new_client_df):
    new_client_df['cod_sesso'] = new_client_df['cod_sesso'].astype('category').cat.codes
    new_client_df['cod_provincia_residenza'] = new_client_df['cod_provincia_residenza'].astype('category').cat.codes

    recommended_list = recommend_coverages(new_client_df)
    # print("Recommended coverages:", recommended_list)

    return recommended_list
