from heapq import heappop, heappush
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
    origin: list
    time: int | float

class Graph:
    def __init__(self, my_map):
        self.graph = {}
        self.solutions = [] #a list of all solutions for each drone different pathway
        self.reserved = []
        self.my_map = my_map
        # Start with the reservation table
        # to see max hub capacity
        # to see max link capacity

    def is_available(self, current_node, at_time):
        check_tuple = (current_node, at_time)
        if self.reserved.count(check_tuple) < self.my_map[current_node].max_drone:
            return True
        return False

    def all_unavailable(self, lst_neighbor, distances):
        check = []
        for elt in lst_neighbor:
            check.append(self.is_available(elt, distances))
        if check.count(False) == len(check):
            return True
        return False


    def shortest_distances(self):
        max_time = len(self.graph) * (self.my_map["nb_drones"] + len(self.reserved) + 2)
        pq = [(0, 0, self.start)]
        distances = {(self.start, 0): 0}
        previous = {(self.start, 0): None}

        while pq:
            current_cost, current_time, current_node = heappop(pq)
            state = (current_node, current_time)
            if current_cost != distances.get(state):
                continue

            if current_node == self.end:
                return self.get_pathway(previous, state)

            if current_time >= max_time:
                continue

            next_time = current_time + 1

            if self.is_available(current_node, next_time):
                wait_state = (current_node, next_time)
                wait_cost = current_cost + 1
                if wait_cost < distances.get(wait_state, float("inf")):
                    distances[wait_state] = wait_cost
                    previous[wait_state] = state
                    heappush(pq, (wait_cost, next_time, current_node))

            for neighbor, weight in self.graph[current_node].items():
                if weight == float("inf"):
                    continue
                if self.is_available(neighbor, next_time) is False:
                    continue
                next_state = (neighbor, next_time)
                next_cost = current_cost + weight
                if next_cost < distances.get(next_state, float("inf")):
                    distances[next_state] = next_cost
                    previous[next_state] = state
                    heappush(pq, (next_cost, next_time, neighbor))

        raise ValueError("Error: Unsolvable map")


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

    def get_pathway(self, previous, goal_state):
        path = []
        current_state = goal_state
        while current_state is not None:
            node, time = current_state
            path.append((time, node))
            current_state = previous[current_state]
        return sorted(path)


    def do_reservation(self, distance: list):
        if len(distance) == 0:
            return
        for elt in distance:
            self.reserved.append((elt[1], elt[0]))


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
