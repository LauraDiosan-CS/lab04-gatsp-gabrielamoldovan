from random import randint, seed

from load_data import fitness


def generateARandomPermutation(n):
    perm = [i for i in range(n)]
    pos1 = randint(0, n - 1)
    pos2 = randint(0, n - 1)
    perm[pos1], perm[pos2] = perm[pos2], perm[pos1]
    return perm


# permutation-based representation
class Chromosome:
    def __init__(self, problParam=None):
        self.__problParam = problParam  # problParam has to store the number of nodes/cities
        self.__repres = generateARandomPermutation(self.__problParam['noNodes'])
        self.__fitness = 0.0

    @property
    def repres(self):
        return self.__repres

    @property
    def fitness(self):
        return self.__fitness

    @repres.setter
    def repres(self, l=[]):
        self.__repres = l

    @fitness.setter
    def fitness(self, fit=0.0):
        self.__fitness = fit

    def crossover(self, c):
        # order XO
        pos1 = randint(-1, self.__problParam['noNodes'] - 1)
        pos2 = randint(-1, self.__problParam['noNodes'] - 1)
        if (pos2 < pos1):
            pos1, pos2 = pos2, pos1
        k = 0
        newrepres = self.__repres[pos1: pos2]
        for el in c.__repres[pos2:] + c.__repres[:pos2]:
            if (el not in newrepres):
                if (len(newrepres) < self.__problParam['noNodes'] - pos1):
                    newrepres.append(el)
                else:
                    newrepres.insert(k, el)
                    k += 1

        offspring = Chromosome(self.__problParam)
        offspring.repres = newrepres
        return offspring

    def mutation(self):
        # insert mutation
        pos1 = randint(0, self.__problParam['noNodes'] - 1)
        pos2 = randint(0, self.__problParam['noNodes'] - 1)
        if (pos2 < pos1):
            pos1, pos2 = pos2, pos1
        el = self.__repres[pos2]
        del self.__repres[pos2]
        self.__repres.insert(pos1 + 1, el)

    def __str__(self):
        return "\nChromo: " + str(self.__repres) + " has fit: " + str(self.__fitness)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, c):
        return self.__repres == c.__repres and self.__fitness == c.__fitness

class Population:

    def __init__(self, params):
        self.__params = params
        self.__repres = []
        for i in range(10):
            self.__repres.append(Chromosome(params))
            self.__repres[i].fitness = fitness(self.__repres[0].repres, params['mat'])

    def mutation(self, i):
        self.__repres[i].mutation()

    def best_fitness(self):
        c= 0
        fit = fitness(self.__repres[0].repres, self.__params['mat'])
        for i in range(1, len(self.__repres)):
            fitc = fitness(self.__repres[i].repres, self.__params['mat'])
            if fitc != 0.0 and fitc < fit or fit == 0.0:
                c = i
        return self.__repres[c]

    def worst_fitness(self):
        c = 0
        fit = fitness(self.__repres[0].repres, self.__params['mat'])
        for i in range(1, len(self.__repres)):
            fitc = fitness(self.__repres[i].repres, self.__params['mat'])
            if fitc > fit:
                c = i
        return self.__repres[c]

    def next_generation(self):
        b1 = self.best_fitness()
        self.__repres.remove(self.best_fitness())
        b2 = self.best_fitness()
        self.__repres.append(b1)
        c = b2.crossover(b1)
        c.mutation()
        c.fitness = fitness(c.repres, self.__params['mat'])
        self.__repres.remove(self.worst_fitness())
        self.__repres.append(c)