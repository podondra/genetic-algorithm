def read_instances(f):
    data = {}
    for line in f.readlines():
        # separator is whitespace and convert to integers
        items = list(map(int, line.split()))
        # key is id
        data[items[0]] = {
                'n': items[1],  # number of items
                'm': items[2],  # capacity
                'weights': items[3::2],  # items weights
                'values': items[4::2]  # items values
                }
    return data


def read_solutions(f):
    data = {}
    for line in f.readlines():
        items = list(map(int, line.split()))
        data[items[0]] = {
            'n': items[1],
            'solution_value': items[2],
            'solution': items[3:]
        }
    return data
