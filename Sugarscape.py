"""Written by Dan Kearney, Natalie Mattison, and Theodore Thompson
for Olin College Computational Modeling 2011."""

from Government import *
from Matrix import Matrix
from Agent import *
import time
import random
import math

class Sugarscape(Matrix):

    def __init__(self, num_agents = 500, max_sugar=5, sugar_growth_rate=.5,
                 agent_vision=3, agent_metabolism=2.5, tax_rate=.5):
        ''' The sugarscape is a matrix of Location objects.'''
        Matrix.__init__(self, 51, 51)
        self.max_sugar = max_sugar
        self.sugar_growth_rate = sugar_growth_rate
        self.agent_vision = agent_vision
        self.agent_metabolism = agent_metabolism
        self.tax_rate = tax_rate
        self.agents = []
        self.total_wealth = 0
        self.num_agents = num_agents
        self.timestamp = 0
        self.gov = Government(tax_rate=self.tax_rate, sugarscape=self)
        self.populate_sugarscape()

    def reset(self):
        '''resets the whole sugarscape'''
        self.agents = []
        self.gov.tax_rate = self.tax_rate
        Matrix.__init__(self,51,51)
        self.agents = []
        self.populate_sugarscape()
        self.timestamp = 0
        return True

    def make_uniform_terrian(self):
        ''' update the blank uniform sugarscape '''
        for x in range(self.length):
            for y in range(self.width):
                loc = self.get_location(x, y)
                loc.set_max_sugar(self.max_sugar)
                loc.set_sugar_amt(self.max_sugar)
                loc.set_sugar_growth_rate(self.sugar_growth_rate)

    def initialize_slope_terrian(self,_value=0):
        for x in range(self.length):
            for y in range(self.width):
                loc = self.get_location(x, y)
                loc.set_max_sugar(_value)

    def add_slope_terrian(self,c_x,c_y,_gradient=0.3):
        for x in range(self.length):
            for y in range(self.width):
                nDistance = math.sqrt((x-c_x)**2 + (y-c_y)**2)
                ratio_max_sugar = (int)(self.max_sugar - _gradient*nDistance)
                if ratio_max_sugar <= 0:
                    ratio_max_sugar = 0
                if ratio_max_sugar >= self.max_sugar:
                    ratio_max_sugar = self.max_sugar
                loc = self.get_location(x, y)
                #print loc.get_max_sugar()
                loc.set_max_sugar(loc.get_max_sugar() + ratio_max_sugar)

    def modify_slope_terrian(self):
        for x in range(self.length):
            for y in range(self.width):
                loc = self.get_location(x, y)
                value = loc.get_max_sugar() + 1
                if value <= 1:
                    value = 1
                if value >= self.max_sugar:
                    value = self.max_sugar
                loc.set_max_sugar(value)
                loc.set_sugar_amt(value)
                
                loc.set_sugar_growth_rate(self.sugar_growth_rate)

    def populate_sugarscape(self):
        '''updates the blank sugarscape to have the attributes we want.
        also, populates the agents.'''
        self.make_uniform_terrian()
        self.initialize_slope_terrian()
        self.add_slope_terrian(15,15)
        self.add_slope_terrian(35,35)
        self.modify_slope_terrian()
        while len(self.agents) < self.num_agents:
            x = random.randint(0, self.length - 1)
            y = random.randint(0, self.width - 1)
            self.add_agent(x, y)
        return True

    def add_agent(self, x, y):
        '''adds an agent to the sugarscape'''
        if not self.get_location(x, y).get_has_agent():
            if random.randint(2) is 0:
                agent = Agent(x, y, self.agent_vision, 2, 'male',self.agent_metabolism, self)
            else
                agent = Agent(x, y, self.agent_vision, 2, 'female',self.agent_metabolism, self)
            self.agents.append(agent)
            return True
        else:
            return False

    def remove_agent(self, agent):
        '''removes an agent from the sugarscape'''
        self.agents.remove(agent)
        return True

    def get_nearby_locations(self, vision, location):
        ''' returns a list of all location objects within
        a certain range of the object'''
        nearby_locations = []
        for i in range(-vision, vision + 1):
            if i==0: continue
            nearby_xloc = self.get_location((location.x + i) % self.length, location.y)
            nearby_yloc = self.get_location(location.x, (location.y + i) % self.width)
            nearby_locations.append(nearby_xloc)
            nearby_locations.append(nearby_yloc)
        return nearby_locations
    
    def nextstep(self):
        '''moves the sugarscape forward one time step.
        Agents and all locations update'''
        for x in range(self.length):
            for y in range(self.width):
                self.get_location(x, y).regrow_sugar()
        self.total_wealth = 0
        for agent in self.agents:
            self.total_wealth += agent.sugar_reserve
        for agent in self.agents:
            agent.nextstep()
        self.timestamp +=1
        if self.timestamp % 1 == 0:
            self.gov.tax()

    def agent_wealths(self):
        ''' makes a list of all agent wealths '''
        wealths = []
        for agent in self.agents:
            wealths.append(agent.get_sugar_reserve())
        return wealths

    def get_location(self, x, y):
        return self.get_value(x,y)

    def set_agent_vision(self, value):
        self.agent_vision = value
        
    def set_tax_rate(self, value):
        self.tax_rate = value
    
    def set_max_sugar(self, value):
        self.max_sugar = value
    
    def set_sugar_growth_rate(self, value):
        self.sugar_growth_rate = value
    
    def set_num_agents(self, value):
        self.num_agents = value
    
    def set_agent_metabolism(self, value):
        self.agent_metabolism = value

    def __str__(self):
        return_str = ""
        for y in range(self.width):
            for x in range(self.length):
                return_str += str(self.get_location(x, y).get_sugar_amt())
                return_str += " "
            return_str += "\n"
        return return_str
    



