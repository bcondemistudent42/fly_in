from .parsing.parsing_class import Hubs


class Dijkstra_Node:
    def __init__(self, name, cost, adjacent_hubs):
        self.visited = False
        self.name = name
        self.true_cost = cost
        self.relative_cost = float("inf")
        self.origin = None
        self.links = adjacent_hubs

def dijkstra_init(my_map, start):
    dct_dij = {}
    for elt in my_map.values():
        if isinstance(elt, Hubs):
            if elt.name == start:
                dct_dij[elt.name] = Dijkstra_Node(elt.name, elt.cost, elt.links["links"])
                dct_dij[elt.name].visited = True
                dct_dij[elt.name].cost = 0
            else:
                dct_dij[elt.name] = Dijkstra_Node(elt.name, elt.cost, elt.links["links"])

    way = []
    work_drone = [x for x in dct_dij.values() if x.visited is True][0]
    while work_drone != "goal" :
        work_drone.visited = True
        for elt in work_drone.links:
            
