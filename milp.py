from svg_dumper import Dumper
from data_model import Graph
from pulp import LpProblem, LpVariable, lpSum, LpMinimize, value

g = Graph()
g.init_cities()
distances = g.get_edges()
n = len(distances)

model = LpProblem("TSP_MILP", sense=LpMinimize)

x = dict()
for i in range(n):
    for j in range(n):
        x[(i, j)] = LpVariable(f"x_{i}_{j}", 0, 1, cat="Binary")
        
for i in range(n):
    constraint = []
    for j in range(n):
        if (i != j):
            constraint.append(x[i, j])
    model += lpSum(constraint) == 1

for j in range(n):
    constraint = []
    for i in range(n):
        if (i != j):
            constraint.append(x[i, j])
    model += lpSum(constraint) == 1

u = []
for i in range(n):
    u.append(LpVariable(name=f"u_{i}", lowBound=0))

for i in range(1, n):
    for j in range(1, n):
        if i != j:
            model += u[i] - u[j] + n * x[i, j] <= n - 1

tgt = []
for i in range(n):
    for j in range(n):
        if i != j:
            tgt.append(distances[i][j] * x[i, j])

model += lpSum(tgt)

model.solve()

print("Total distance:", value(model.objective))

result = [[0 for _ in range(n)] for _ in range(n)]
for v in model.variables():
    vname = v.name.split('_')
    if vname[0] == 'x' and v.varValue == True:
        i, j = int(vname[1]), int(vname[2])
        result[i][j] = distances[i][j]


d = Dumper()
d.set_cities(g.get_cities())
d.set_matrix(result)
d.render('milp.svg', by_matrix=True)
