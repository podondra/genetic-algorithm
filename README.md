# Genetic Algorithm

Genetic algorithm implementation applied to knapsack and SAT problems.

## SAT Instances

3-SAT instances are in file `data/sat-instances.csv`.
For more information about them please refer to report.
They can be parsed using `pandas`:

```
import pandas

instances = pandas.read_csv('data/sat-instances.csv', index_col=[0, 1])
instances.index.names = [None, None]
instances.head()
```
