import numpy
import random
from deap import algorithms, tools


def evaluate_constrain(individual, weights, m):
    return sum(x * w for x, w in zip(individual, weights)) <= m


def genetic_algorithm(population, toolbox, ngen, cxpb, mutpb, elitism):
    # statistics
    stats = tools.Statistics(lambda individual: individual.fitness.values)
    stats.register('min', numpy.min)
    stats.register('max', numpy.max)
    stats.register('avg', numpy.mean)
    stats.register('std', numpy.std)
    # logbook
    logbook = tools.Logbook()
    logbook.header = ['gen', 'new', 'min', 'max', 'avg', 'std']

    # evaluate the entire population
    fitnesses = map(toolbox.evaluate, population)
    for individual, fitness in zip(population, fitnesses):
        individual.fitness.values = fitness

    # halloffame
    halloffame = tools.HallOfFame(maxsize=elitism)
    halloffame.update(population)

    # individual to select by toolbox.select fuction
    # rest is for elite individuals
    n_select = len(population) - len(halloffame)

    # TODO implement stopping criterium
    # begin the evolution
    for g in range(1, ngen + 1):
        # select the next generation individuals
        offspring = toolbox.select(population, k=n_select)
        # clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # apply crossover and mutation on the offspring
        offspring = algorithms.varAnd(offspring, toolbox, cxpb, mutpb)

        # evaluate the individuals with an invalid fitness
        invalids = [i for i in offspring if not i.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalids)
        for individual, fitness in zip(invalids, fitnesses):
            individual.fitness.values = fitness

        # replace the current population by the offspring
        population[:] = offspring + halloffame.items

        halloffame.update(population)

        # append the current generation statistics to the logbook
        record = stats.compile(population)
        logbook.record(gen=g, new=len(invalids), **record)
        print(logbook.stream)

    return population, logbook, halloffame


def evaluate_penalization(individual, weights, values, m):
    total_weight = 0
    total_value = 0
    for x, weight, value in zip(individual, weights, values):
        total_weight += x * weight
        total_value += x * value
    if total_weight > m:
        return -total_weight,
    return total_value,


def correct_individual(individual, weights, m):
    while evaluate_constrain(individual, weights, m) is False:
        indexes = [index for index, x in enumerate(individual) if x]
        individual[random.choice(indexes)] = 0
    return individual


def evaluate_correction(individual, weights, values, m):
    individual = correct_individual(individual, weights, m)
    total_value = 0
    for x, value in zip(individual, values):
        total_value += x * value
    return total_value,
