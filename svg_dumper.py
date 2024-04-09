from math import sin, cos, isclose
from math import pi as PI_CONST
from regions import bolshevik, kaliningrad, komsomolets, mainland, october_revolution, sakhaline, severny_novaya_zemlya, wrangel, yuzhny_novaya_zemlya

# gnomic projection
def getCleanProjection(location):
    lat0 = PI_CONST / 2
    long0 = 0
    
    
    lat1 = location[0] * (PI_CONST / 180)
    long1 = location[1] * (PI_CONST / 180)
    
    cos_c = sin(lat0) * sin(lat1) + cos(lat0) * cos(long1 - long0)
    x = (cos(lat0) * sin(lat1) - sin(lat0) * cos(lat1) * cos(long1 - long0)) / cos_c
    y = (cos(lat1) * sin(long1 - long0)) / cos_c
    return x, y


class Dumper:
    
    def __init__(self):
        self.regions_ = []
        self.bbox_ = [[0, 0], [0, 0]]
        self.header_top_ = '<svg version="1.1" width="1200" height="1000" xmlns="http://www.w3.org/2000/svg">\n'
        self.header_bottom_ = '</svg>'
        self.offset_ = [100, 100]
        self.locations_ = [[]]
        self.way_ = []
        self.matrix_ = [[]]
    
    def set_cities(self, locations):
        self.locations_ = locations
        
    def set_way(self, way):
        self.way_ = way
        
    def set_matrix(self, matrix):
        self.matrix_ = matrix.copy()
        
    def init_regions(self):
        self.regions_.append(bolshevik.bolshevik)
        self.regions_.append(kaliningrad.kaliningrad)
        self.regions_.append(komsomolets.komsomolets)
        self.regions_.append(mainland.mainland)
        self.regions_.append(october_revolution.october_revolution)
        self.regions_.append(sakhaline.sakhaline)
        self.regions_.append(severny_novaya_zemlya.severny_novaya_zemlya)
        self.regions_.append(wrangel.wrangel)
        self.regions_.append(yuzhny_novaya_zemlya.yuzhny_novaya_zemlya)

    def render(self, filename, by_matrix=False):
        if len(self.regions_) == 0:
            self.init_regions()
        
        self.calculateBbox()
        svg_data = self.header_top_
        svg_data += self.render_regions()
        svg_data += self.render_locations()
        
        if (by_matrix):
            svg_data += self.render_matrix()
        else:
            svg_data += self.render_way()
        
        svg_data += self.header_bottom_
        f = open(filename, 'w')
        f.write(svg_data)
        f.close()

    def render_arc(self, point1, point2, color):
        point1 = self.projectionWithOffset(point1)
        point2 = self.projectionWithOffset(point2)
        svg_data = ''
        svg_data += '<line vector-effect="non-scaling-size" x1="' + str(point1[0]) + '" y1="' + str(point1[1]) + '" '
        svg_data += 'x2="' + str(point2[0]) + '" y2="' + str(point2[1]) +'" '
        svg_data += 'style="stroke: ' + color + ' ;stroke-width:1" />\n'
        return svg_data
                
    def render_regions(self):
        svg_data = ''
        for region in self.regions_:
            for i in range(len(region)):
                svg_data += self.render_arc(region[i], region[(i + 1) % len(region)], 'red')
        return svg_data
    
    def render_locations(self):
        # print (self.locations_)
        svg_data = ''
        for location in self.locations_:
            # print(location)
            location = self.projectionWithOffset(location)
            svg_data += '<circle cx="' + str(location[0]) + '" cy="' + str(location[1]) + '" r="3" style="fill:green;stroke:black;stroke-width:1" />\n'
        return svg_data

    def render_way(self):
        svg_data = ''
        for i in range(len(self.way_)):
            city1 = self.way_[i]
            city2 = self.way_[(i + 1) % len(self.way_)]
            svg_data += self.render_arc(city1, city2, 'blue')
        return svg_data

    def render_matrix(self):
        svg_data = ''
        for i in range(len(self.matrix_[0])):
            for j in range(len(self.matrix_)):
                if isclose(self.matrix_[j][i], 1.0):
                    svg_data += self.render_arc(self.locations_[j], self.locations_[i], 'black')
                elif isclose(self.matrix_[j][i], 0.5):
                    svg_data += self.render_arc(self.locations_[j], self.locations_[i], 'red')
                elif self.matrix_[j][i] > 0.5:
                    svg_data += self.render_arc(self.locations_[j], self.locations_[i], 'blue')
                
        return svg_data
    
    def projectionWithOffset(self, location):
        lat0 = PI_CONST / 2
        long0 = 0
        
        lat1 = location[0] * (PI_CONST / 180)
        long1 = location[1] * (PI_CONST / 180)

        cos_c = sin(lat0) * sin(lat1) + cos(lat0) * cos(long1 - long0)
        x = (cos(lat0) * sin(lat1) - sin(lat0) * cos(lat1) * cos(long1 - long0)) / cos_c
        y = (cos(lat1) * sin(long1 - long0)) / cos_c
        return 600 * (x - self.bbox_[0][0]) + self.offset_[0], 600 * (y - self.bbox_[0][1]) + self.offset_[1]

    def calculateBbox(self):
        found = False
        for region in self.regions_:
            for location in region:
                point = getCleanProjection(location)
                if not found:
                    self.bbox_ = [point, point]
                    found = True
                else:
                    self.bbox_[0] = [min(self.bbox_[0][0], point[0]), min(self.bbox_[0][1], point[1])]
                    self.bbox_[1] = [max(self.bbox_[1][0], point[0]), max(self.bbox_[1][1], point[1])] # remove this ??
