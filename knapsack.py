version = "1.0.1"

class ReproductionFailedError(Exception):
    def __init__(self, fits, CAP, POP):
        super().__init__(f"Population unable to reproduce.\n"
                         f"\tAmount of sets with positive fitness is less than 2: {fits}\n"
                         f"\tTry increasing the following values: CAP={CAP}, POP={POP}")

class ValueDataTypeError(Exception):
    def __init__(self, name, value):
        super().__init__(f"Invalid data type.\n"
                         f"\tValue {name}={value} must be an int.")

class ValueScopeError(Exception):
    def __init__(self, name, value):
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
        raise ReproductionFailedError(fits, CAP, POP)
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
    best_i = []
    max_val = max(fits)
    for i in range(POP):
        if fits[i] == max_val:
            best_sets.append(pop[i])
            best_i.append(i)
    return max_val, best_sets, best_i

def main():
    if not isinstance(CAP, int):
        raise ValueDataTypeError("CAP",CAP)
    if not isinstance(POP, int):
        raise ValueDataTypeError("POP",POP)
    if not isinstance(GEN, int):
        raise ValueDataTypeError("GEN",GEN)
    if not (0 <= CROSS <=1):
        raise ValueScopeError("CROSS", CROSS)
    if not (0 <= MUT <=1):
        raise ValueScopeError("MUT", MUT)
    if POP < 2:
        raise PopulationSizeError
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
        print(f"GENETARTION {gen}")
        for i in range(POP):
            print(f"{i+1}. {" "*(len(str(POP))-len(str(i+1)))}{r[0][i]} FITNESS={r[1][i]}")
        print(f"\tBEST:\tFITNESS={r[2][0]}")
        for i in range(len(r[2][2])):
            print(f"\t{r[2][2][i]+1}. {" "*(len(str(POP))-len(str(r[2][2][i]+1)))}{r[2][1][i]}")
        gen += 1

tui(main())
