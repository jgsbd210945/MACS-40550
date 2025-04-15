from model import SugarScapeModel
from mesa.visualization import Slider, SolaraViz, make_plot_component
from mesa.visualization.components.matplotlib_components import make_mpl_space_component

## Define agent portrayal (color, size, shape)
def agent_portrayal(agent):
    return {"marker": "o", 
            "color": "red", 
            "size": 20}

## Define map portrayal, with yellower squares having more sugar than white squares
propertylayer_portrayal = {
    "sugar": {"color": "yellow", 
              "alpha": 0.8, 
              "colorbar": True, 
              "vmin": 0, 
              "vmax": 10},
}

## Define model space component based on above
sugarscape_space = make_mpl_space_component(
    agent_portrayal=agent_portrayal,
    propertylayer_portrayal=propertylayer_portrayal,
    post_process=None,
    draw_grid=False,
)

## Define Gini plot
GiniPlot = make_plot_component("Gini")

## Define variable model parameters
model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "width": 50,
    "height": 50,
    "initial_population": Slider(
        "Initial Population", value=200, min=50, max=500, step=10
    ),
    # Agent endowment parameters
    "endowment_min": Slider("Min Initial Endowment", value=10, min=5, max=20, step=1), # Changed to make scaling work
    "endowment_max": Slider("Max Initial Endowment", value=30, min=20, max=50, step=1),
    # Metabolism parameters
    "metabolism_min": Slider("Min Metabolism", value=1, min=1, max=2, step=1),
    "metabolism_max": Slider("Max Metabolism", value=3, min=2, max=5, step=1), # Changed to make scaling work
    # Vision parameters
    "vision_min": Slider("Min Vision", value=1, min=1, max=3, step=1),
    "vision_max": Slider("Max Vision", value=5, min=3, max=8, step=1),
    # Initial Movemement Parameters
    "move_min": Slider("Min Initial Movement", value=1, min=1, max=2, step=1), # Initial Movement (accounting for genetics, etc.)
    "move_max": Slider("Max Initial Movement", value=3, min=2, max=5, step=1),
}

##Instantiate model
model = SugarScapeModel()

## Define all aspects of page
page = SolaraViz(
    model,
    components=[
        sugarscape_space,
        GiniPlot,
    ],
    model_params=model_params,
    name="Sugarscape",
    play_interval=150,
)
## Return page
page