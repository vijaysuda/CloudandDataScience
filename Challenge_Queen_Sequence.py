
# coding: utf-8

# In[10]:


import numpy as np
import sys

num_queen = 8
terminatep= 28
mutating= 0.000001
generate_mutate_flag= True
high_iter = 100000
POPULATION = None

class QueenPosition:
    def __init__(self):
        self.sequence = None
        self.fit_score = None
        self.survival = None
    def setSequence(self, val):
        self.sequence = val
    def setfit_score(self, fit_score):
        self.fit_score = fit_score
    def setSurvival(self, val):
        self.survival = val
    def getAttr(self):
        return {'sequence':sequence, 'fit_score':fit_score, 'survival':survival}

def fit_score(chromosome = None):
    clashes = 0;
    row_col_clashes = abs(len(chromosome) - len(np.unique(chromosome)))
    clashes += row_col_clashes

	# calculate diagonal clashes
    for i in range(len(chromosome)):
        for j in range(len(chromosome)):
            if ( i != j):
                dx = abs(i-j)
                dy = abs(chromosome[i] - chromosome[j])
                if(dx == dy):
                    clashes += 1


    return 28 - clashes	


def getSequence():
	# randomly generates a sequence of board states.
    global num_queen
    init_distribution = np.arange(num_queen)
    np.random.shuffle(init_distribution)
    return init_distribution

def getPopulation(population_size = 100):
    global POPULATION

    POPULATION = population_size

    population = [QueenPosition() for i in range(population_size)]
    for i in range(population_size):
        population[i].setSequence(getSequence())
        population[i].setfit_score(fit_score(population[i].sequence))

    return population


def retriveParent():
    globals()	
    parent1, parent2 = None, None
    summation_fit_score = np.sum([x.fit_score for x in population])
    for each in population:
        each.survival = each.fit_score/(summation_fit_score*1.0)

    while True:
        parent1_random = np.random.rand()
        parent1_rn = [x for x in population if x.survival <= parent1_random]
        try:
            parent1 = parent1_rn[0]
            break
        except:
            pass

    while True:
        parent2_random = np.random.rand()
        parent2_rn = [x for x in population if x.survival <= parent2_random]
        try:
            t = np.random.randint(len(parent2_rn))
            parent2 = parent2_rn[t]
            if parent2 != parent1:
                break
            else:
                print("equal parents")
                continue
        except:
            print("exception")
            continue

    if parent1 is not None and parent2 is not None:
        return parent1, parent2
    else:
        sys.exit(-1)

def generate_cross(parent1, parent2):
    globals()
    n = len(parent1.sequence)
    c = np.random.randint(n, size=1)
    child = QueenPosition()
    child.sequence = []
    child.sequence.extend(parent1.sequence[0:c])
    child.sequence.extend(parent2.sequence[c:])
    child.setfit_score(fit_score(child.sequence))
    return child


def generate_mutate(child):
    if child.survival < generate_mutate:
        c = np.random.randint(8)
        child.sequence[c] = np.random.randint(8)
    return child

def geneticAlgo(iteration):
    print(" #"*10 ,"Executing Genetic  generation : "), iteration , " #"*10
    globals()
    newpopulation = []
    for i in range(len(population)):
        parent1, parent2 = retriveParent()
        # print("Parents generated : "), parent1, parent2

        child = generate_cross(parent1, parent2)

        if(generate_mutate_FLAG):
            child = generate_mutate(child)

        newpopulation.append(child)
    return newpopulation


def terminate():
    globals()
    fit_scorevals = [pos.fit_score for pos in population]
    if terminatep in fit_scorevals:
        return True
    if high_iter == iteration:
        return True
    return False



population = getPopulation(1000)

print("POPULATION size : "), population

iteration = 0;
while not terminate():
    population = geneticAlgo(iteration)
    iteration +=1 

print("Iteration number : "), iteration
for each in population:
    if each.fit_score == 28:
        print(each.sequence)

