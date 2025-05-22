import math
import random
import networkx as nx

import mesa
from mesa import Model
from agents import State, CountryAgent

# Helper functions for metrics
def number_state(model, state):
    return sum(1 for a in model.grid.get_all_cell_contents() if a.state is state)

def num_dems(model):
    return number_state(model, State.DEM)

def num_autos(model):
    return number_state(model, State.AUTO)

def num_greys(model):
    return number_state(model, State.GREY)


class CountryNetwork(Model):
    def __init__(
        self,
        num_nodes=50, # Needs to be a bit higher for the level we're at. Max should prolly be...200?
        avg_node_degree=10, # b/c we have more nodes, will need more connections (Especially in an international environment)
        seed=None,
        dem_levels=0.3,
        consol_levels=0.5,
        type_split=0.5,
        power_change=0.05,
    ):
        super().__init__(seed=seed)
        random.seed(seed)

        # Model-level Variables
        self.type_split = type_split
        self.power_change = power_change

        # Initializing these as dummy variables so we can reassign later.
#        self.democracy = dem_levels
#        self.consolidation = consol_levels
#        self.power = 0.5

        # Network Setup
        self.num_nodes = num_nodes
        prob = avg_node_degree / self.num_nodes

        # I am not going to be doing a weighted network *as things stand*, I'm focused on power, which is in
        # the agent class.
        # HOWEVER I might do it in the future? But I'm not sure quite yet.
        self.G = nx.erdos_renyi_graph(n=self.num_nodes, p=prob)
        for u, v in self.G.edges():
            self.G.edges[u, v]['weight'] = 1  

        # Get list of edge weights and node positions; used for visualization
        # (This is taken from L7, but it's for visualization, so not sure if this is "adapting")
        self.weights = [2*self.G[u][v]['weight'] for u, v in self.G.edges]
        self.position = nx.circular_layout(self.G)

        # Create grid from network object
        self.grid = mesa.space.NetworkGrid(self.G)

        # Data collection. Mostly to track number of regimes and pct consolidaiton
        self.datacollector = mesa.DataCollector(
            {
                "Democracies": num_dems,
                "Autocracies": num_autos,
                "Grey": num_greys,
            }
        )

        # Create agents
        for node in self.G.nodes():
            a = CountryAgent(
                self,

                # Tentatively using beta distributions for consolidation and democracy. May change as needed.
                # Idea: a, b = 0, 1; k = 1; mu = input parameter.
                # Ergo: alpha = input param, beta = 1 - input param. No need to scale since it's between 0 and 1.
                self.random.betavariate(consol_levels, (1 - consol_levels)), # Consolidation

                # Democracy is the same, using average LEVEL of democracy as the mean. ## DO BIMODAL???
                self.random.betavariate(dem_levels, (1 - dem_levels)), # Democracy

                # Power (Currently) is random, uniformly distributed (do normal dist?)
                self.random.random(), # Power
            )

            # Add the agent to the node
            self.grid.place_agent(a, node)


        self.running = True
        self.datacollector.collect(self)

    # Step function (Basic idea, I'll need to flesh this out)
    def step(self):
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)