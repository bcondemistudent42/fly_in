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

    def is_available(self, current_node, distances):
        check_tuple = (current_node, distances[current_node].time)
        # print(check_tuple)
        # print(self.reserved)
        # print()
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
        # print(f"reserved =={self.reserved}")
        distances = {node: NodeData(float("inf"), None, float("inf")) for node in self.graph}
        # to see if it's good to put float("inf") as time default value
        distances[self.start] = NodeData(0, None, 0)

        pq = [(0, self.start)]
        heapify(pq)

        visited = set()

        while pq:
            current_distance, current_node = heappop(pq)

            if (current_node, distances[current_node].time) in visited:
                continue
            visited.add((current_node, distances[current_node].time))


            # print(self.check_available_time(current_node, distances))
            # if self.check_available_time(current_node, distances) is False:
            #     distances[current_node].time += 1
            #     heappush(pq, (current_distance + 1, current_node))

            lst_neighbor = []
            for neighbor, weight in self.graph[current_node].items():
                lst_neighbor.append(neighbor)

                next_node_distance = current_distance + weight

                temp_cost = distances[neighbor].cost
                temp_origin = distances[neighbor].origin
                temp_time = distances[neighbor].time

                if next_node_distance < distances[neighbor].cost:
                    distances[neighbor].cost = next_node_distance
                    distances[neighbor].origin = current_node
                    distances[neighbor].time = distances[current_node].time + 1

                    # reset node function with value before the assignation
                    if self.is_available(neighbor, distances) is False:
                        distances[neighbor].cost = temp_cost
                        distances[neighbor].origin = temp_origin
                        distances[neighbor].time = temp_time + 1
                        
                        distances[current_node].time += 1
                        heappush(pq, (current_distance + 1, current_node))
                        
                        continue
                    if len(pq) == 0 and self.all_unavailable(lst_neighbor, distances):
                        distances[current_node].time += 1
                        heappush(pq, (current_distance + 1, current_node))
                    else:
                        heappush(pq, (next_node_distance, neighbor))

        if distances[self.end].origin is None:
            raise ValueError("Error: Unsolvable map")
        return distances, self.get_pathway(distances)


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
        goal = self.end
        path = []

        while goal is not None:
            path.append((goal, distance[goal].time))
            goal = distance[goal].origin
        path = path[::-1]
        return path


    def do_reservation(self, distance):
        work_hub = self.end
        if len(distance) == 0:
            return
        while work_hub is not None:
            self.reserved.append((work_hub, distance[work_hub].time))
            work_hub = distance[work_hub].origin



    # def get_pathway_clean(self, distance): to see for more
    #     path = []
    #     visited = set()
    #     max_steps = len(self.graph) + 1
    #     step_count = 0
        
    #     current_node = self.end

    #     while current_node is not None:
    #         if current_node in visited:
    #             raise ValueError(f"Cycle detected in path at node '{current_node}'")
    #         if step_count > max_steps:
    #             raise ValueError(f"Path reconstruction exceeded max steps ({max_steps})")
            
    #         visited.add(current_node)
    #         path.append(current_node)
    #         current_node = distance[current_node].origin
    #         step_count += 1
    #     if path[-1] != self.start:
    #         raise ValueError(f"Path does not reach start node '{self.start}'")
    #     path.reverse()
    #     return path


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
