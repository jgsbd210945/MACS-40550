from mesa import Agent
import statistics

class SchellingAgent(Agent):
    ## Initiate agent instance, inherit model trait from parent class
    def __init__(self, model, axis0, axis1, desired_share_alike):
        super().__init__(model)
        ## Set agent type
        self.type0 = axis0
        self.type1 = axis1
        self.desired_share_alike = desired_share_alike
    ## Define basic decision rule
    def move(self):
        ## Get list of neighbors within range of sight
        neighbors = self.model.grid.get_neighbors(self.pos, moore = True)
        ## Count neighbors of same type as self
        ## If an agent has any neighbors (to avoid division by zero), calculate share of neighbors of same type
        if neighbors:
            sum_neighbor = [0, 0]
            for neighbor in neighbors:
                sum_neighbor[0] += ((self.type0 == neighbor.type0) + (self.type1 == neighbor.type1))
                sum_neighbor[1] += 2
            share_alike = sum_neighbor[0]/sum_neighbor[1]
        else:
            share_alike = self.desired_share_alike
        ## If unhappy with neighbors, move to random empty slot. Otherwise add one to model count of happy agents.
        if share_alike < self.desired_share_alike:
            self.model.grid.move_to_empty(self)
        else:
            self.model.happy += 1
