import mesa
import math
import solara
import networkx as nx
from matplotlib.figure import Figure
from model import State, CountryNetwork
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
    "dem_levels": Slider(
        label="Average Level of Democracy",
        value=0.5,
        min=0,
        max=1,
        step=0.05,
    ),
    "consol_levels": Slider(
        label="Average Consolidation Level",
        value=0.5,
        min=0,
        max=1,
        step=0.05,
    ),    
    "type_split": Slider(
        label="% Chance of Democratization",
        value=0.5,
        min=0,
        max=1,
        step=0.05,
    ),
    "power_change": Slider(
        label="Power Shift Magnitude",
        value=0.1,
        min=0,
        max=0.5,
        step=0.01,
    ),
}

# Colors. Need to ensure color dict works here.
def agent_portrayal(agent):
    node_color_dict = {
        State.AUTO: "red",
        State.GREY: "gray",
        State.DEM: "blue",
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
#DistributionGraph = make_plot_component() # Need to flesh this out

def post_process_lineplot(ax):
    ax.set_ylim(ymin=0)
    ax.set_ylabel("# states")
    ax.legend(bbox_to_anchor=(1.05, 1.0), loc="upper left")

StatePlot = make_plot_component(
    {"Autocracies": "red", "Grey": "gray", "Democracies": "blue"},
    post_process=post_process_lineplot,
)

@solara.component
def get_dem_level(model):
    update_counter.get()
    dem_lvl = model.dem_level()
    dem_lvl_txt = r"$\infty$" if dem_lvl is math.inf else f"{dem_lvl:.3f}"
    
    return solara.Markdown(f"Average Democracy Level: {dem_lvl_txt}")

@solara.component
def get_consol_level(model):
    update_counter.get()
    consol_lvl = model.consol_level()
    consol_lvl_txt = r"$\infty$" if consol_lvl is math.inf else f"{consol_lvl:.3f}"
    
    return solara.Markdown(f"Average Consolidation Level: {consol_lvl_txt}")

# Do I want an overall level of democracy? Could be useful
# Could also do a total level of consolidation.

# Initialize model instance
model1 = CountryNetwork()

# Define page components
page = SolaraViz(
    model1,
    components=[
        NetPlot,
        StatePlot,
        get_dem_level,
        get_consol_level,
    ],
    model_params=model_params,
    name="Consolidation Model",
)
# Return page
page 