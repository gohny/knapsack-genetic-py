# Genetic algorithm for [knapsack problem](https://en.wikipedia.org/wiki/Knapsack_problem) written in python
Version: `1.0.3`
## Usage
### Variables
- `ITEMS` - List of tuples containing item data (format: `({weight}, {value})`).
- `CAP` - Capacity of the knapsack.
- `POP` - Population size.
- `GEN` - Amount of generations (including initial generation).
- `CROSS` - Probability of each pair of parents crossing their genes (scope: `0-1`).
- `MUT` - Probability of mutation of each gene (scope: `0-1`).

Adjust these variables to get different results.
### Output
Prints sets of each generation and `fitness` of each set.  
Points out best sets with the highest `fitness` for each generation.

`fitness` - Value of each set (when it exceeds `CAP` its value is set to `0`).
#### Example
```
GENERATION {generation number}
1. [{set of genes}] FITNESS={fitness of first set}
2. [{set of genes}] FITNESS={fitness of second set}
3. [{set of genes}] FITNESS={fitness of third set}
  BEST: FITNESS={best fitness of current generation}
  {No.} [{set of genes}]
```
***
Made by gohny
