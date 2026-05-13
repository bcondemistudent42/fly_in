from heapq import heapify, heappop, heappush
from .parsing.parsing_class import Hubs

from dataclasses import dataclass

@dataclass
class Connection:
    hub_1: str
    hub_2: str
    capacity: int

@dataclass
class NodeData:
    cost: int | float
    origin: str | None

class Graph:
    def __init__(self, graph: dict = {}):
        self.graph = graph
        self.solutions = [] #a list of all solutions for each drone different pathway 

    def shortest_distances(self):
        distances = {node: NodeData(float("inf"), None) for node in self.graph}
        distances[self.start] = NodeData(0, None)

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
                if next_node_distance < distances[neighbor].cost:
                    distances[neighbor].cost = next_node_distance
                    distances[neighbor].origin = current_node
                    heappush(pq, (next_node_distance, neighbor))

        if distances[self.end].origin is None:
            raise ValueError("Error: Unsolvable map")
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

    def get_pathway(self, distance):
        goal = distance[self.end]
        path = []

        path.append(self.end)
        while goal.origin is not None:
            path.append(str(goal).split("origin='")[1].replace("')", "").strip())
            goal = distance[goal.origin]
        path = path[::-1]
        return path


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
