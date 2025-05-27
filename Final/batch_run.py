from mesa.batchrunner import batch_run

from model import CountryNetwork

import pandas as pd

power_params = {
    "num_nodes": list(range(50, 250, 25)),
    "avg_node_degree": 10,
    "consol_levels": 0.5,
    "type_split": 0.5,
    "power_change": list(i/40 for i in range(1, 11)), # 0.025 -> 0.25
    "seed": list(range(10)),
    "dem_levels": 0.5
}

dem_consol_params = {
    "num_nodes": list(range(50, 250, 50)),
    "avg_node_degree": 10,
    "consol_levels": list(i/20 for i in range(1, 20)), # 19?
    "type_split": 0.5,
    "power_change": 0.1,
    "seed": list(range(10)),
    "dem_levels": list(i/20 for i in range(1, 20))
}

if __name__ == '__main__':
    power_results = batch_run(
        CountryNetwork,
        parameters=power_params,
        iterations=5,
        max_steps=100,
        number_processes=None,
        data_collection_period=1,
        display_progress=True

    )
    df_1 = pd.DataFrame(power_results)
    df_1.to_csv("power_results.csv", index=False)

    demcons_results = batch_run(
        CountryNetwork,
        parameters=dem_consol_params,
        iterations=5,
        max_steps=100,
        number_processes=None,
        data_collection_period=1,
        display_progress=True

    )
    df_2 = pd.DataFrame(demcons_results)
    df_2.to_csv("demcons_results.csv", index=False)