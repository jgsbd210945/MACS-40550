from enum import Enum

from mesa import Agent

#Define enumeration of susceptibility state
class State(Enum):
    SUSCEPTIBLE = 0
    INFECTED = 1
    RESISTANT = 2


class VirusAgent(Agent):
    #Define initiation of agents
    def __init__(
        self,
        model,
        initial_state,
        virus_spread_chance,
        virus_check_frequency,
        recovery_chance,
        gain_resistance_chance
    ):
        super().__init__(model)

        self.state = initial_state
        self.virus_spread_chance = virus_spread_chance
        self.virus_check_frequency = virus_check_frequency
        self.recovery_chance = recovery_chance
        self.gain_resistance_chance = gain_resistance_chance
    # Infected agents try to spread virus to connected agents
    def try_to_infect_neighbors(self):
        # Get connected nodes
        neighbors_nodes = self.model.grid.get_neighborhood(
            self.pos, include_center=False
        )
        # From connected nodes, get list of susceptible neighbors
        susceptible_neighbors = [
            agent
            for agent in self.model.grid.get_cell_list_contents(neighbors_nodes)
            if agent.state is State.SUSCEPTIBLE
        ]
        # Try to infect neighbors subject to two probabilities: edge weight and global virus spread chance
        for a in susceptible_neighbors:
            if self.random.random() < self.model.grid.G.edges[self.pos, a.pos]['weight']:
                if self.random.random() < self.virus_spread_chance:
                    a.state = State.INFECTED

    # Agent gains resistance subject to global probability. Called upon sick agents becoming uninfected
    def try_gain_resistance(self):
        if self.random.random() < self.gain_resistance_chance:
            self.state = State.RESISTANT

    # Infected agents become uninfected subject to global probability. If uninfected, try to gain resistance. Called if agent checks situation
    def try_remove_infection(self):
        # Try to remove
        if self.random.random() < self.recovery_chance:
            # Success
            self.state = State.SUSCEPTIBLE
            self.try_gain_resistance()
        else:
            # Failed
            self.state = State.INFECTED

    # Agent randomly checks to see if infected, dubject to global probability. If infected, tries to remove infection
    def try_check_situation(self):
        if (self.random.random() < self.virus_check_frequency) and (
            self.state is State.INFECTED
        ):
            self.try_remove_infection()
    # Agent step: Infected agents try to spread virus, all agents check situation
    def step(self):
        if self.state is State.INFECTED:
            self.try_to_infect_neighbors()
        self.try_check_situation()