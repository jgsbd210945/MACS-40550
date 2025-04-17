from pathlib import Path

import numpy as np

import mesa
from agents import SugarAgent
## Using experimental cell space for this model that enforces von Neumann neighborhoods
from mesa.experimental.cell_space import OrthogonalVonNeumannGrid
from mesa.experimental.cell_space import HexGrid
## Use experimental space feature that allows us to save sugar as a property of the grid spaces
from mesa.experimental.cell_space.property_layer import PropertyLayer

class SugarScapeModel(mesa.Model):
    ## Helper function to calculate Gini coefficient, used in plot
    def calc_gini(self):
        agent_sugars = [a.sugar for a in self.agents]
        sorted_sugars = sorted(agent_sugars)
        n = len(sorted_sugars)
        x = sum(el * (n - ind) for ind, el in enumerate(sorted_sugars)) / (n * sum(sorted_sugars))
        return 1 + (1 / n) - 2 * x
    ## Define initiation, inherit seed property from parent class
    def __init__(
        self,
        width = 50,
        height = 50,
        initial_population=200,
        endowment_min=10,
        endowment_max=30,
        metabolism_min=1,
        metabolism_max=3,
        vision_min=1,
        vision_max=5,
        move_min=1,
        move_max=3,
        seed = None
    ):
        super().__init__(seed=seed)
        ## Instantiate model parameters
        self.width = width
        self.height = height
        ## Set model to run continuously
        self.running = True
        ## Create grid
        self.grid = HexGrid(
            (self.width, self.height), torus=False, random=self.random
        )
        ## Define datacollector, which calculates current Gini coefficient
        self.datacollector = mesa.DataCollector(
            model_reporters = {"Gini": self.calc_gini},
        )
        ## Import sugar distribution from raster, define grid property
        self.sugar_distribution = np.genfromtxt(Path(__file__).parent / "sugar-map.txt")
        self.grid.add_property_layer(
            PropertyLayer.from_data("sugar", self.sugar_distribution)
        )
        ## Create agents, give them random properties, and place them randomly on the map
        SugarAgent.create_agents(
            self,
            initial_population,
            self.random.choices(self.grid.all_cells.cells, k=initial_population),
            sugar=self.rng.integers(
                endowment_min, endowment_max, (initial_population,), endpoint=True
            ),
            metabolism=self.rng.integers(
                metabolism_min, metabolism_max, (initial_population,), endpoint=True
            ),
            vision=self.rng.integers(
                vision_min, vision_max, (initial_population,), endpoint=True
            ),
            movement = self.rng.integers(
                move_min, move_max, (initial_population,), endpoint=True
            ),
        )
        ## Initialize datacollector
        self.datacollector.collect(self)
    ## Define step: Sugar grows back at constant rate of 1, all agents move, then all agents consume, then all see if they die. Then model calculated Gini coefficient.
    def step(self):
        self.grid.sugar.data = np.minimum(
            self.grid.sugar.data + 1, self.sugar_distribution
        )
        
        self.agents.shuffle_do("move") # Simultaneous Activation
        self.agents.shuffle_do("gather_and_eat")
        self.agents.shuffle_do("see_if_die")
        self.datacollector.collect(self)
    
