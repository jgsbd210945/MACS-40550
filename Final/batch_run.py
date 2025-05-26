from mesa.batchrunner import batch_run

from model import CountryNetwork

import pandas as pd

params = {
    "num_nodes": list(range(50, 250, 20)),
    "avg_node_degree": 10,
    "consol_levels": 0.5,
    "type_split": 0.5,
    "power_change": list(i/40 for i in range(1, 10)), # 0.025 -> 0.25
    "seed": list(range(10)),
    "dem_levels": list(i/20 for i in range(1, 19))
}

if __name__ == '__main__':
    results = batch_run(
        CountryNetwork,
        parameters=params,
        iterations=5,
        max_steps=100,
        number_processes=None,
        data_collection_period=1,
        display_progress=True

    )
    df = pd.DataFrame(results)
    df.to_csv("results.csv", index=False)