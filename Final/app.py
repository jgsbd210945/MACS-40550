import mesa
import math
import solara
import networkx as nx
from matplotlib.figure import Figure
from model import CountryNetwork
from mesa.visualization import (
    Slider,
    SolaraViz,
    make_plot_component,
    make_space_component,
)
from mesa.visualization.utils import update_counter

# Define model parameters
model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "num_nodes": Slider(
        label="Number of agents",
        value=50,
        min=25,
        max=250,
        step=5,
    ),
    "avg_node_degree": Slider(
        label="Avg Node Degree",
        value=10,
        min=5,
        max=50,
        step=1,
    ),
}

def agent_portrayal(agent):
    node_color_dict = {
        # Need to figure out how to model democracy/autocracy/grey. Could do a State but in that case I'd need to reformat
        # how I'm doing this, and I'm not sure if I want to do that.
    }
    return node_color_dict[agent.state]

# Create custom figure to plot the network graph (used in order to plot weighted edges)
# (Adapted from L7 as well, though again, it's doing a similar thing)
@solara.component
def NetPlot(model):
    # Set this to update every turn, define it as mpl figure
    update_counter.get()
    fig = Figure()
    ax = fig.subplots()
    
    # Need to figure out colors here. Not entirely certain just what I'm gonna do (categorical, ranged).
    color_dict = {}
    for node in model.G.nodes():
        color_dict[node] = agent_portrayal(model.grid.get_cell_list_contents([node])[0])
    # Get list of colors for each node based on dictionary
    node_colors = [color_dict[node] for node in model.G.nodes()]


    # Draw network graph based on colors defined here and node positions/edge weights defined in the model
    nx.draw(model.G,
            ax=ax,
            pos = model.position,
            node_color=node_colors,
            width = model.weights)
    # Plot the figure
    solara.FigureMatplotlib(fig)

# I'll want a stacked bar graph of democracies/autocracies/grey over time. Will need to set that up.
DistributionGraph = make_plot_component() # Need to flesh this out

# Do I want an overall level of democracy? Could be useful
# Could also do a total level of consolidation.

# Initialize model instance
model1 = CountryNetwork()

# Define page components
page = SolaraViz(
    model1,
    components=[NetPlot], # I don't think I need anything else *yet*, just need to do the viz for democracies.
    model_params=model_params,
    name="Consolidation Model",
)
# Return page
page 