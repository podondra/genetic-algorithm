import pandas
from matplotlib import pyplot
import itertools


def sample_instances(instances, n_samples):
    random.seed(16)
    index = []
    for s in instance_sizes:
        index += list(itertools.product([s],
                      random.sample(range(499), n_samples)))
    return instances.loc[index]


def relative_error(c_opt, c_apx):
    return (c_opt - c_apx) / c_opt


def plot_ga_progress(logbook, optimum):
    gs = logbook.select('gen')
    mins = logbook.select('min')
    avgs = logbook.select('avg')
    maxs = logbook.select('max')

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
