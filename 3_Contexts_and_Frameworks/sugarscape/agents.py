import math
## Using experimental agent type with native "cell" property that saves its current position in cellular grid
from mesa.experimental.cell_space import CellAgent

## Helper function to get distance between two cells
def get_distance(cell_1, cell_2):
    x1, y1 = cell_1.coordinate
    x2, y2 = cell_2.coordinate
    dx = x1 - x2
    dy = y1 - y2
    return math.sqrt(dx**2 + dy**2)

class SugarAgent(CellAgent):
    ## Initiate agent, inherit model property from parent class
    def __init__(self, model, cell, sugar=0, metabolism=0, vision = 0, movement = 0):
        super().__init__(model)
        ## Set variable traits based on model parameters
        self.cell = cell
        self.sugar = sugar
        self.metabolism = metabolism
        self.vision = vision
        self.movement = movement
    ## Define movement action
    def move(self):
        for iter in range(self.movement):
            ## Determine currently empty cells within line of sight
            possibles = [
                cell
                for cell in self.cell.get_neighborhood(self.vision, include_center=True)
                if cell.is_empty 
            ]
            ## Determine how much sugar is in each possible movement target
            sugar_values = [
                cell.sugar
                for cell in possibles
            ]
            ## Calculate the maximum possible sugar value in possible targets
            max_sugar = max(sugar_values)
            ## Get indices of cell(s) with maximum sugar potential within range
            candidates_index = [
                i for i in range(len(sugar_values)) if math.isclose(sugar_values[i], max_sugar)
            ]
            ## Indentify cell(s) with maximum possible sugar
            candidates = [
                possibles[i]
                for i in candidates_index
            ]
            ## Find the closest cells with maximum possible sugar
            min_dist = min(get_distance(self.cell, cell) for cell in candidates)
            final_candidates = [
                cell
                for cell in candidates
                if math.isclose(get_distance(self.cell, cell), min_dist, rel_tol=1e-02)
            ]
            ## Choose one of the closest cells with maximum sugar (randomly if more than one)
            self.cell = self.random.choice(final_candidates)
    ## consumer sugar in current cell, depleting it, then consumer metabolism
    def gather_and_eat(self):
        self.sugar += self.cell.sugar
        self.cell.sugar = 0

        # At the same time, what I'll do is update movement/metabolism based on the amount of sugar someone overall has.

        # I'm updating sugar based on base metabolism and *also* how much a specific agent moves.
        # So moving 1 doesn't change, moving 2 or 3 increases by 1, and so on. Trying to make this not too overpowering.
        self.sugar -= (self.metabolism + math.floor(0.5 * self.movement))
        
        # Now, what can we do is also affect the amount someone can move based on the amount of sugar they have, with 1 being the base.
        self.movement = 1 if self.sugar < 5 else round(self.sugar / 10)
        # Rounding *should* even it out...
        # BUT if they have less than 5 sugar...they should be able to move a little until they die.

    ## If an agent has zero or negative sugar, it dies and is removed from the model
    def see_if_die(self):
        if self.sugar <= 0:
            self.remove()
    
    
        