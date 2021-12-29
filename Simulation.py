import numpy as np
import random

class Simulation:
    def __init__(self, evaluation_function, mutate_agent):
        self.mutate_agent = mutate_agent
        self.calculate_fitness = evaluation_function
        self.best_agents = [([], float('-inf'), -1)] #Agent, fitness, epoch [([], float('-inf'), -1)]
        
    def calculate_fitness_array(self, agents, points):
        fitnesses = np.array([self.calculate_fitness(agent, points) for agent in agents])
        return fitnesses
    
    def calculate_diversity_score_array(self, agents): #This takes >10x longer than the rest of the code combined. Figure out a way to optimize it.
        if np.all(np.equal.reduce(agents, axis=0)):   #Check to make sure not all agents are the same
            return np.zeros(shape = agents.shape[0])
        
        return np.array([np.mean(np.linalg.norm(agents-agent, axis=1)) for agent in agents])
        #return np.array([np.mean(np.equal(agents, agent)) for agent in agents])
        
    def calculate_reproduction_chance(self, population, value_uniqueness = 0.5):
        fitnesses = self.calculate_fitness_array(population.agents, population.points)
        non_norm_fitnesses = np.copy(fitnesses)
        
        if value_uniqueness > 0:
            non_norm_uniquenesses = self.calculate_diversity_score_array(population.agents)
        
        #print(self.best_agents)
        if max(fitnesses) > self.best_agents[-1][1]:
            self.best_agents.append((population.agents[np.argmax(fitnesses)], max(fitnesses), population.epoch))
        
        fitnesses = (fitnesses-np.mean(fitnesses))/np.std(fitnesses)

        
        if value_uniqueness > 0:
            gene_uniqueness = np.copy(non_norm_uniquenesses)
            gene_uniqueness = (gene_uniqueness-np.mean(gene_uniqueness))/np.std(gene_uniqueness)

            reproduction_chance = fitnesses + (gene_uniqueness * value_uniqueness)
            reproduction_chance = (reproduction_chance-np.mean(reproduction_chance))/np.std(reproduction_chance)

            return reproduction_chance+2, non_norm_fitnesses, non_norm_uniquenesses

        return fitnesses+2, non_norm_fitnesses, 0

    def distance(self, x1, x2):
        return np.linalg.norm(x1-x2)

    def mutate_array(self, agents, rate, bounds):
        mutated_agents = np.array([self.mutate_agent(agent, rate=rate, bounds=bounds) for agent in agents])
        return mutated_agents

    def merge_genes(self, a, b, n_genes):
        if n_genes <= 1:
            return a
        
        #merged = np.zeros(shape=(n_genes, a.shape[0], int(a.shape[1]/n_genes)))
    
        genes_a = a.reshape(n_genes, a.shape[0], int(a.shape[1]/n_genes))
        genes_b = b.reshape(n_genes, a.shape[0], int(b.shape[1]/n_genes))
        to_merge = np.random.randint(0,2, size=(n_genes))

        merged[to_merge == 0] = genes_a[to_merge == 0]
        merged[to_merge == 1] = genes_b[to_merge == 1]

        return merged.reshape(a.shape[0], a.shape[1])

    def next_generation(self, population, mutation_rate=0.01, value_diversity = 0.5, show_fitness = False, show_diversity = False):

        fitnesses, fitness_array, diversity_array = self.calculate_reproduction_chance(population, value_uniqueness=value_diversity)
        gene_pool = np.array(random.choices(population.agents, weights = fitnesses, k=population.agents.shape[0]*2))

        next_gen = np.array([self.merge_genes(gene_pool[i], gene_pool[i+1], population.num_genes) for i in range(int(len(gene_pool)/2))])
        next_gen = self.mutate_array(next_gen, mutation_rate, population.bounds)
        
        if show_fitness and show_diversity:
            fitness = np.mean(fitness_array)
            diversity = np.mean(diversity_array)
            return next_gen, fitness, diversity
        if show_fitness:
            fitness = np.mean(fitness_array)
            return next_gen, fitness
        if show_diversity:
            diversity = np.mean(diversity_array)
            return next_gen, diversity
        return next_gen