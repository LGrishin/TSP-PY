from math import sin, cos, sqrt
from cities import cities

def to_spherical(city):
    radian = 0.0174533
    thetta = (90 - city[0]) * radian
    phi = city[1] * radian
    return thetta, phi


# distance between city1 and city2
def distance(city1, city2):
    earth_radius = 6356.752
    thetta1, phi1 = to_spherical(city1)
    thetta2, phi2 = to_spherical(city2)
    rq = 2 * earth_radius * earth_radius
    return sqrt(rq - rq * (sin(thetta1) * sin(thetta2) * cos(phi1 - phi2) + cos(thetta1) * cos(thetta2)))

def way_len(cities):
    result = 0
    for i in range(len(cities)):
        city1 = cities[i]
        city2 = cities[(i+1) % len(cities)]
        result += distance(city1, city2)
    return result

def matrix_way_len(matrix):
    result = 0
    for row in matrix:
        for el in row:
            result += el
    return result

class Graph:
    def __init__(self):
        self.edges_ = [[]]
        self.cities_ = []
    
    def init_cities(self):
        size = len(cities)
        self.edges_ = [[0 for _ in range(size)] for _ in range(size)]
        self.cities_ = [(0, 0) for _ in range(size)]
        self.read_data_dict(cities)

    def get_cities(self):
        return self.cities_
    
    def get_edges(self):
        return self.edges_
    
    def read_data_dict(self, cities_dict):
        indx = 0
        for key in cities_dict.keys():
            self.cities_[indx] = (cities_dict[key][0], cities_dict[key][1])
            indx += 1

        for i in range(len(self.cities_)):
            for j in range(len(self.cities_)):
                if i != j:
                    self.add_edge(i, j, distance(self.cities_[i], self.cities_[j]))
    
    def add_edge(self, u, v, weight):
        self.edges_[u][v] = weight
        self.edges_[v][u] = weight

