version = "1.0.2"

class Errors:
    @staticmethod
    def var_name(var):
        vars = {"CAP":CAP, "POP":POP, "GEN":GEN, "CROSS":CROSS, "MUT":MUT}
        for key, value in vars.items():
            if var is value:
                return key

    class ReproductionFailedError(Exception):
        def __init__(self, fits, CAP, POP):
            super().__init__(f"Population unable to reproduce.\n"
                             f"\tAmount of sets with positive fitness is less than 2: {fits}\n"
                             f"\tTry increasing the following values: CAP={CAP}, POP={POP}")

    class ValueDataTypeError(Exception):
        def __init__(self, value):
            name = Errors.var_name(value)
            super().__init__(f"Invalid data type.\n"
                             f"\tValue {name}={value} must be an int.")

    class ValueScopeError(Exception):
        def __init__(self, value):
            name = Errors.var_name(value)
            super().__init__(f"Value out of scope.\n"
                             f"\tValue {name}={value} must be in a scope 0-1.")

    class PopulationSizeError(Exception):
        def __init__(self, POP):
            super().__init__(f"Population too small.\n"
                             f"\tPopulation size must be greater than 1.\n"
                             f"\tIncrease the following value: POP={POP}")

import random

ITEMS = [(10,4), (5,2), (4,1), (4,3), (15,5), (3,1), (10,6), (13, 7), (8, 5), (6, 3)]

CAP = 50
POP = 10
GEN = 10
CROSS = 0.7
MUT = 0.2

def generate():
    return [random.randint(0,1) for _ in range(len(ITEMS))]

def fitness(pop):
    fits = []
    for i in pop:
        total_weight = 0
        total_value = 0
        for j in range(len(ITEMS)):
            if i[j] == 1:
                weight, value = ITEMS[j]
                total_weight += weight
                total_value += value
        if total_weight > CAP:
            fits.append(0)
        else:
            fits.append(total_value)
    if sum(fits) == max(fits):
        raise Errors.ReproductionFailedError(fits, CAP, POP)
    return fits

def roulette (pop, fits):
    wheel = []
    for i in range(POP-1):
        if i == 0:
            wheel.append(fits[i])
        wheel.append(wheel[i]+fits[i+1])
    i = 0
    last = None
    pair = []
    while i < 2:
        pick = random.uniform(0, wheel[-1])
        for j in range(POP):
            find = wheel[j]
            if find >= pick:
                if find == wheel[j-1] or j == last:
                    break
                else:
                    i += 1
                    last = j
                    pair.append(pop[j])
                    break
    return pair

def cross(p1, p2):
    if random.random() < CROSS:
        index = len(ITEMS)//2
        c1 = p1[:index] + p2[index:]
        c2 = p2[:index] + p1[index:]
        return [c1,c2]
    else:
        return [p1,p2]

def mutate(set):
    for i in range(len(ITEMS)):
        if random.random() < MUT:
            set[i] = 1 - set[i]
    return set

def best(pop, fits):
    best_sets = []
    best_indices = []
    best_fit = max(fits)
    for i in range(POP):
        if fits[i] == best_fit:
            best_sets.append(pop[i])
            best_indices.append(i)
    return best_fit, best_sets, best_indices

def main():
    for i in [CAP, POP, GEN]:
        if not isinstance(i, int):
            raise Errors.ValueDataTypeError(i)
    for i in [CROSS, MUT]:
        if not (0 <= i <=1):
            raise Errors.ValueScopeError(i)
    if POP < 2:
        raise Errors.PopulationSizeError
    pop = []
    parents = []
    for i in range(POP):
        pop.append(generate())
    fits = fitness(pop)
    for i in range(GEN):
        parents.clear()
        for j in range(int(POP/2)):
            parents += roulette(pop, fits)
        pop.clear()
        for j in range(POP):
            if j%2 == 0:
                pop += cross(parents[j], parents[j+1])
        for j in range(POP):
                pop[j] = mutate(pop[j])
        fits = fitness(pop)
        yield pop, fits, best(pop, fits)

def tui(result):
    gen = 1
    for r in result:
        pop = r[0]
        fits = r[1]
        best_fit = r[2][0]
        best_sets = r[2][1]
        best_indices = r[2][2]
        print(f"GENETARTION {gen}")
        for i in range(POP):
            print(f"{i+1}. {" "*(len(str(POP))-len(str(i+1)))}{pop[i]} FITNESS={fits[i]}")
        print(f"\tBEST:\tFITNESS={best_fit}")
        for i in range(len(best_indices)):
            print(f"\t{best_indices[i]+1}. {" "*(len(str(POP))-len(str(best_indices[i]+1)))}{best_sets[i]}")
        gen += 1
tui(main())
