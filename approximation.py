from svg_dumper import Dumper, getCleanProjection
from data_model import Graph, way_len
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
from shapely.geometry import LineString
from tqdm import tqdm

class Dfs:
    def __init__(self, matrix, cities):
        self.matrix_ = matrix
        self.visited_ = [False for _ in range(len(self.matrix_[0]))]
        self.cities_ = cities
        self.way_ = []

    def run(self, current):
        if self.visited_[current]:
            return
        self.way_.append(self.cities_[current])
        self.visited_[current] = True
        for i in range(len(self.visited_)):
            if self.matrix_[current][i] or self.matrix_[i][current]:
                self.run(i)

    def get_way(self):
        return self.way_


def check_intersection(locations):
    size = len(locations)
    for i in range(size):
        c2 = getCleanProjection(locations[i])
        c1 = getCleanProjection(locations[(i + 1) %  size])
        first = LineString([c1, c2])
    
        for j in range( size):
            c1 = getCleanProjection(locations[j])
            c2 = getCleanProjection(locations[(j + 1) %  size])
            second = LineString([c1, c2])
            if i == j or i == (j + 1) % size or j == (i + 1) % size:
                continue
            if first.intersects(second):
                return [(i + 1) % size, j]
    return [-1, -1]

def reverse(array, pair):
    i = pair[0]
    j = pair[1]
    if i > j:
        i, j = j, i
    section = array[i:j+1]
    section.reverse()
    array[i:j+1] = section
    return array

def optimize(cities):
    cities = list(cities)
    pair = check_intersection(cities)
    # print(cities)

    while (pair != [-1, -1]):
        # print(pair)
        cities = reverse(cities, pair)
        pair = check_intersection(cities)
        # return cities
    return cities
        
g = Graph()
g.init_cities()


X = csr_matrix(g.edges_)

#build spanning tree
spanning_tree_matrix = minimum_spanning_tree(X)
spanning_tree_matrix = spanning_tree_matrix.toarray().astype(bool)

cities = g.get_cities()
# init best way len
best_len = way_len(cities)
best_case = cities
# fing len for each city
for i in tqdm(range(len(cities))):
    dfs = Dfs(spanning_tree_matrix, cities)
    # run dfs
    dfs.run(i)
    
    new_way = dfs.get_way()
    # delete intersections
    new_way = optimize(new_way)
    # update best value if need
    if (best_len > way_len(new_way)):
        best_len = way_len(new_way)
        best_case = new_way

print(best_len)
d = Dumper()
d.set_cities(best_case)
d.set_matrix(spanning_tree_matrix)
d.render('spanning_tree.svg', by_matrix=True)

d.set_way(best_case)
d.render('approximation.svg', by_matrix=False)

a = [0, 1, 2, 3, 4, 5, 6, 7, 8]
a = a[:3:] + a[6:2:-1] + a[7::]
print(a)