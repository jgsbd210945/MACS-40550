import mesa
import math
import solara
import networkx as nx
from matplotlib.figure import Figure
from model import (
    State,
    VirusOnNetwork,
    number_infected,
)
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
        value=10,
        min=10,
        max=100,
        step=1,
    ),
    "avg_node_degree": Slider(
        label="Avg Node Degree",
        value=3,
        min=3,
        max=8,
        step=1,
    ),
    "network_type": {
        "type": "Select",
        "value": "single",
        "values": ["single", "weighted"],
        "label": "Network Type",
    },
    "initial_outbreak_size": Slider(
        label="Initial Outbreak Size",
        value=1,
        min=1,
        max=10,
        step=1,
    ),
    "virus_spread_chance": Slider(
        label="Virus Spread Chance",
        value=0.4,
        min=0.0,
        max=1.0,
        step=0.1,
    ),
    "virus_check_frequency": Slider(
        label="Virus Check Frequency",
        value=0.4,
        min=0.0,
        max=1.0,
        step=0.1,
    ),
    "recovery_chance": Slider(
        label="Recovery Chance",
        value=0.3,
        min=0.0,
        max=1.0,
        step=0.1,
    ),
    "gain_resistance_chance": Slider(
        label="Gain Resistance Chance",
        value=0.5,
        min=0.0,
        max=1.0,
        step=0.1,
    ),
}

# Map colors to agent statuses. Note that syntax is different from standard agent_portrayal, because this is used in a custom figure
def agent_portrayal(agent):
    node_color_dict = {
        State.INFECTED: "red",
        State.SUSCEPTIBLE: "yellow",
        State.RESISTANT: "blue",
    }
    return node_color_dict[agent.state]

# Create custom figure to plot the network graph (used in order to plot weighted edges)
@solara.component
def NetPlot(model):
    # Set this to update every turn, define it as mpl figure
    update_counter.get()
    fig = Figure()
    ax = fig.subplots()
    # Get dictionary mapping individual nodes to colors based on infection status
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

# Helper function adding axis titles and legend to line plot
def post_process_lineplot(ax):
    ax.set_ylim(ymin=0)
    ax.set_ylabel("# people")
    ax.legend(bbox_to_anchor=(1.05, 1.0), loc="upper left")

# Make line plot showing levels of agent statuses over time
StatePlot = make_plot_component(
    {"Infected": "red", "Susceptible": "yellow", "Resistant": "blue"},
    post_process=post_process_lineplot,
)

# Get and display as text the resistant to susceptible ratio
def get_resistant_susceptible_ratio(model):
    ratio = model.resistant_susceptible_ratio()
    ratio_text = r"$\infty$" if ratio is math.inf else f"{ratio:.2f}"
    infected_text = str(number_infected(model))

    return solara.Markdown(
        f"Resistant/Susceptible Ratio: {ratio_text}<br>Infected Remaining: {infected_text}"
    )

# Initialize model instance
model1 = VirusOnNetwork()

# Define page components
page = SolaraViz(
    model1,
    components=[
        NetPlot,
        StatePlot,
        get_resistant_susceptible_ratio,
    ],
    model_params=model_params,
    name="Virus Model",
)
# Return page
page 