from mesa.batchrunner import batch_run

from model import CountryNetwork
from agents import State

import pandas as pd

rand_params = {
    "num_nodes": 50,
    "avg_node_degree": 10,
    "consol_levels": 0.5,
    "type_split": 0.5,
    "power_change": 0.1,
    "seed": list(range(50)),
    "dem_levels": 0.5
}

dem_params = {
    "num_nodes": 50,
    "avg_node_degree": 10,
    "consol_levels": 0.5,
    "type_split": 0.5,
    "power_change": 0.1,
    "seed": 42,
    "dem_levels": list(i/20 for i in range(1, 19)) # Varied levels of democracy
}

def nstate(model, state):
    return sum(1 for i in model.grid.get_all_cell_contents() if i.state == state)

if __name__ == '__main__':
    rand_results = batch_run(
        CountryNetwork,
        parameters=rand_params,
        iterations=5,
        max_steps=100,
        number_processes=None,
        data_collection_period=1,
        display_progress=True

    )
    df_rand = pd.DataFrame(rand_results)
    df_rand.to_csv("rands.csv", index=False)

    dem_results = batch_run(
        CountryNetwork,
        parameters=dem_params,
        iterations=5,
        max_steps=100,
        number_processes=None,
        data_collection_period=1,
        display_progress=True

    )
    df_dem = pd.DataFrame(dem_results)
    df_dem.to_csv("demlvl.csv", index=False)