import sys
# print(sys.path)
import pandas as pd
from collections import defaultdict 
import pulp as p


def load_data():
    adjacents = [[0] * v for l in range(v)]

    total_neighbors = map.neighbors_index
    total_weights = map.total_weight

    for k in range(v):
        neighbors = [(n) for n in total_neighbors[k].split('|')]
        weights = [(n) for n in total_weights[k].split('|')]

        for l in range(len(neighbors)):
            if len(neighbors[l]) == 0 or len(weights[l]) == 0:
                continue
            n = int(neighbors[l]) - 1
            adjacents[k][n] = float(weights[l])
            adjacents[n][k] = float(weights[l])

    return adjacents


def tap30(source, dest):
    Lp_prob = p.LpProblem('Problem', p.LpMinimize) 

    variables = [[0] * v for l in range(v)]

    obj_fun = p.lpSum([0])
    for i in range(v):
        for j in range(v):
            if adjacents[i][j] == 0:
                continue
            
            x = p.LpVariable('x' + str(i) + 'qq' + str(j) , lowBound=0 , upBound = 1, cat='Integer')
            variables[i][j] = x
            obj_fun += adjacents[i][j] * x 
    Lp_prob += obj_fun

    for i in range(v):
        conOut = p.lpSum([0])
        conIn = p.lpSum([0])
        for j in range(v):
            conOut += variables[i][j]
            conIn += variables[j][i]
            if j > i:
                Lp_prob += variables[i][j] + variables[j][i] <= 1

        if i == source:
            Lp_prob += conOut == 1
        elif i == dest:
            Lp_prob += conIn == 1
        else:
            Lp_prob += conOut <= 1
            Lp_prob += conIn <= 1
            Lp_prob += conIn - conOut == 0
            # print(conIn - conOut == 0)
    # print('obj fun', Lp_prob.objective)
    # print(Lp_prob.constraints)
    return (Lp_prob.solve(), variables)


source = int(sys.argv[1]) #int(input("source: "))
dest = int(sys.argv[2]) #int(input("destination: "))

map = pd.read_csv('map.csv')
v = len(map.place_index)
adjacents = load_data()

result, variables = tap30(source, dest)

# print(variables[12])

# for i in range(v):
#         for j in range(v):
#             if type(variables[i][j]) is int:
#                 continue
#             print(variables[i][j].name, variables[i][j].varValue)


path = [source]
i = source
while i != dest:
    for j in range(v):
        if type(variables[i][j]) is int:
                continue

        if variables[i][j].varValue == 1:
            i = j
            path.append(j)
            break

print(*path, sep='-')