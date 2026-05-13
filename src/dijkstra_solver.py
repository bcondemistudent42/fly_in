from heapq import heapify, heappop, heappush
from .parsing.parsing_class import Hubs

from dataclasses import dataclass

@dataclass
class Connection:
    hub_1: str
    hub_2: str
    capacity: int


class Graph:
    def __init__(self, graph: dict = {}):
        self.graph = graph

    def shortest_distances(self):
         distances = {node: float("inf") for node in self.graph}
         distances[self.start] = 0

         pq = [(0, self.start)]
         heapify(pq)

         visited = set()

         while pq:
             current_distance, current_node = heappop(pq)

             if current_node in visited: #to add here later the available and capacity
                continue
             visited.add(current_node)

             for neighbor, weight in self.graph[current_node].items():
                 next_node_distance = current_distance + weight
                 if next_node_distance < distances[neighbor]:
                     distances[neighbor] = next_node_distance
                     heappush(pq, (next_node_distance, neighbor))

         return distances


    def dijkstra_init(self, my_map, start, end):
        hub_lst = [x for x in my_map.values() if isinstance(x, Hubs)]
        
        my_dict = {}
        for hub in hub_lst:
            my_dict[hub.name] = {}
            for link in my_map[hub.name].links["weight"]:
                my_dict[hub.name][link[1]] = my_map[link[1]].cost

        self.graph = my_dict
        self.start = start
        self.end = end


# {'A': {'B': 3, 'C': 3},
# 'B': {'A': 3, 'D': 3.5, 'E': 2.8},
# 'C': {'A': 3, 'E': 2.8, 'F': 3.5},
# 'D': {'B': 3.5, 'E': 3.1, 'G': 10},
# 'E': {'B': 2.8, 'C': 2.8, 'D': 3.1, 'G': 7},
# 'F': {'G': 2.5, 'C': 3.5},
# 'G': {'F': 2.5, 'E': 7, 'D': 10}}
# 


def convert_to_connection(my_map):
    output = []
    for elt in my_map.values():
        if isinstance(elt, list):
            output = [
                Connection(x[0].split("-")[0], x[0].split("-")[1], x[1])
                for x in elt
                if isinstance(x, tuple)
            ]
    return output
