from enum import Enum

from mesa import Agent

# States for democracy
class State(Enum):
    AUTO = 0
    GREY = 1
    DEM = 2

class CountryAgent(Agent):
    def __init__(
        self,
        model,
        consolidation,
        democracy,
        power,
    ):
        super().__init__(model)

        self.consolidation = consolidation
        self.democracy = democracy
        self.power = power
        self.state = State.DEM if self.democracy >= 0.7 else State.AUTO if self.democracy < 0.3 else State.GREY
            # Want to do by color here on the graph so it's clear.

    def interact(self): # interact with neighbor and etc.
        neighbor_nodes = self.model.grid.get_neighborhood(self.pos, include_center = False)

        neighbors = [agent for agent in self.model.grid.get_cell_list_contents(neighbor_nodes)]

        other = self.random.choice(neighbors) # Who does the agent interact with?

        # If regimes match, consolidation increases by 0.1. If two 'grey area' states interact, though, this
        # doesn't change, since they're both in the middle, attempting to push down consolidation in the middle.
        # Additionally, if the other state's power is greater than its own, it will decrease in consolidation, signaling
        # a challenget to its system of governance by a more powerful neighbor.
        if self.state == other.state and self.state != State.GREY:
            self.consolidation += 0.1
        elif other.power > self.power:
            self.consolidation -= 0.1
        
        # Bounding (so it doesn't go negative infinitely)
        if self.consolidation < 0:
            self.consolidation = 0
        elif self.consolidation > 1:
            self.consolidation = 1

    def update(self):
        # If a random number is greater than the amount a state is NOT consolidated (therefore making it easy
        # to change probabilities based on consolidation)
        # Then, it will have a chance to shift more or less democratic.
        if self.random.random() > (1 - self.consolidation):
            self.consolidation -= 0.05 # Further instability = further decrease in consolidation.

            if self.random.random() > self.model.type_split:
                self.democracy += self.random.uniform(0.05, (1 - self.consolidation)) # democratizing episode
            else:
                self.democracy -= self.random.uniform(0.05, (1 - self.consolidation)) # autocratizing episode
            
            # Bounding
            if self.democracy < 0:
                self.democracy = 0
            if self.democracy > 1:
                self.democracy = 1

        # If the state doesn't shift its regime, it gets another bonus in its consolidation level.
        else:
            self.consolidation += 0.05

        # Update regime: Democracy if dem level is above .7, autocracy if it's below 0.3, grey if it's somewhere in between.
        self.state = State.DEM if self.democracy >= 0.7 else State.AUTO if self.democracy < 0.3 else State.GREY
        
        self.power += self.random.uniform((self.model.power_change * -1), self.model.power_change)

        # Bounding
        if self.power < 0:
            self.power = 0
        if self.power > 1:
            self.power = 1


    # Steps! Agent interacts with a random neighbor and then updates.
    def step(self):
        self.interact()
        self.update()
        # Do I also want to have a chance to add further interactions here? i.e. adding or cutting a link so that
        # The networks change?
