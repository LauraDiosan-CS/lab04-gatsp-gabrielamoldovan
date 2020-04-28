from GA import Population
from load_data import read_file


def run():
    mat = read_file("easy.txt")
    population = Population(mat)
    for i in range(1000):
        population.next_generation()
    c = population.best_fitness()
    print(c)

run()
