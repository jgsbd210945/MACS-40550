from mesa.batchrunner import batch_run

from model import CountryNetwork

import pandas as pd

## What I'm doing is doing an even more fine-grained split on democracy levels. I'm going from 0.01 to 0.99.
dem_params = {
    "num_nodes": list(range(50, 250, 50)),
    "avg_node_degree": 10,
    "consol_levels": 0.5,
    "type_split": 0.5,
    "power_change": 0.1,
    "seed": list(range(10)),
    "dem_levels": list(i/100 for i in range(1, 100))
}

if __name__ == '__main__':
    dem_results = batch_run(
        CountryNetwork,
        parameters=dem_params,
        iterations=5,
        max_steps=100,
        number_processes=None,
        data_collection_period=1,
        display_progress=True

    )
    dem_df = pd.DataFrame(dem_results)
    dem_df.to_csv("dem_results.csv", index=False)