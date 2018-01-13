import numpy
import pandas
from matplotlib import pyplot
import itertools


def read_sat_instances(files):
    instances = {}
    numpy.random.seed(74)
    for file in files:
        i = int(file[15:-4])
        n, m, cnf = parse_dimacs(file)
        for m in [50, 106, 162, 218]:
            instances[(m, i)] = {
                'n': n,
                'm': m,
                'formula': cnf[:m],
                'weights': numpy.random.randint(1, 1024 + 1, size=n),
            }
    instances = pandas.DataFrame.from_dict(instances).T
    instances['m'] = instances['m'].astype(numpy.int)
    instances['n'] = instances['n'].astype(numpy.int)
    instances['ratio'] = instances['m'] / instances['n']
    return instances


def sat_fitness(individual, cnf, weights):
    m = len(cnf)
    # evaluate formula
    satisfied_clauses = 0
    for clause in cnf:
        for v in clause:
            idx = abs(v) - 1
            bit = individual[idx]
            if (v < 0 and bit == 0) or (v > 0 and bit == 1):
                satisfied_clauses += 1
                break
    # if satisfied sum weights
    if m == satisfied_clauses:
        return (sum(v * w for v, w in zip(individual, weights)),)
    else:
        return (satisfied_clauses - m,)


def parse_dimacs(dimacs_file):
    with open(dimacs_file) as f:
        # read comments and problem line
        for line in f:
            # ignore comments
            if line[0] == 'c':
                continue
            if line[0] == 'p':
                _, _, variables, clauses = line.split()
                n, m = int(variables), int(clauses)
                break
        raw_formula = iter(f.read().split())
    formula = []
    # for each clause
    for j in range(m):
        clause = []
        while True:
            var = int(next(raw_formula))
            # append variables to a clause until 0
            if var == 0:
                formula.append(clause)
                break
            clause.append(var)
    return n, m, formula


def sample_instances(instances, n_samples):
    random.seed(16)
    index = []
    for s in instance_sizes:
        index += list(itertools.product([s],
                      random.sample(range(499), n_samples)))
    return instances.loc[index]


def relative_error(c_opt, c_apx):
    return (c_opt - c_apx) / c_opt


def plot_ga_progress(logbook, optimum=None):
    gs = logbook.select('gen')
    mins = logbook.select('min')
    avgs = logbook.select('avg')
    maxs = logbook.select('max')

    if optimum:
        pyplot.axhline(optimum, label='optimum', color='red')

    pyplot.scatter(gs, maxs, label='max', marker='.')
    pyplot.scatter(gs, avgs, label='avg', marker='.')
    pyplot.scatter(gs, mins, label='min', marker='.')
    pyplot.xlabel('generation')
    pyplot.ylabel('fitness')
    pyplot.grid()
    pyplot.legend()


def read_instance(file):
    data = {}
    for line in file.readlines():
        # separator is whitespace and convert to integers
        items = list(map(int, line.split()))
        # key is id
        data[(items[1], items[0])] = {
                'm': items[2],  # capacity
                'weights': items[3::2],  # items weights
                'values': items[4::2]  # items values
                }
    return data


def read_solution(file):
    data = {}
    for line in file.readlines():
        items = list(map(int, line.split()))
        data[(items[1], items[0])] = {
            'value': items[2],
            'solution': items[3:]
        }
    return data


def read_instances(files):
    data_dict = {}
    for instance_path, solution_path in files:
        with open(instance_path) as file:
            instances = read_instance(file)
        with open(solution_path) as file:
            solutions = read_solution(file)
        for k, v in instances.items():
            v.update(solutions[k])
        data_dict.update(instances)
    return pandas.DataFrame.from_dict(data_dict, orient='index')
