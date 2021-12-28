import numpy as np
import matplotlib.pyplot as plt

class Population:
    def __init__(self, agents=[], agent_length=None, num_agents=None, bounds=None, num_genes=1, starting_bounds=None):
        self.agents = agents
        self.num_genes = num_genes
        
        self.fitness_history = []
        self.diversity_history = []
        self.epoch = 0
        self.points = np.random.rand(agent_length, 2) * (bounds[1]-bounds[0]) + bounds[0]
        
        if agent_length == None:
            self.agent_length = agents.shape[1]
        else:
            self.agent_length = agent_length
            
        if num_agents == None:
            self.num_agents = agents.shape[0]
        else:
            self.num_agents = num_agents
            
        if bounds == None:
            self.bounds = (min(agents), max(agents))
        else:
            self.bounds = bounds
            
        if starting_bounds == None:
            self.starting_bounds = self.bounds
        else:
            self.starting_bounds = starting_bounds
            
        self.reset()
        
    def reset(self):
        self.fitness_history = []
        self.diversity_history = []
        self.epoch = 0
        self.agents = self.generate_agents(self.agent_length, self.num_agents)
        
    def next_generation(self, agents, mean_fitness = None, mean_diversity = None):
        self.agents = agents
        self.epoch += 1
        if not (mean_fitness is None):
            self.fitness_history.append(mean_fitness)
        if not (mean_diversity is None):
            self.diversity_history.append(mean_diversity)
    
    def generate_agents(self, agent_length, num_agents):
        x = np.arange(agent_length)
        y = np.arange(num_agents)
        z, l = np.meshgrid(x,y)
        for agent in z:
            np.random.shuffle(agent)
        return z
        #return np.random.randint(0,2, size=(num_agents, 4, agent_length))
    
    def define_visualization_function(self, f):
        self.visualize = f
        
    def display(self):
        self.visualize(self)
    
    def save_img(self, name):
        fig = self.visualize(self)
        fig.savefig(f'Output/{name}.jpg')
        plt.close(fig)