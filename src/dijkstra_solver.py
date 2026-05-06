from .parsing.parsing_class import Hubs


class Dijkstra_Node:
    def __init__(self, name, cost, adjacent_hubs):
        self.visited = False
        self.name = name
        self.true_cost = cost
        self.relative_cost = float("inf")
        self.origin = None
        self.links = adjacent_hubs


def dijkstra_init(map, start, end, reserved, drone_name):

    work_hub = Dijkstra_Node(map[start].name, map[start].cost, map[start].links["links"])
    work_hub.visited = True
    work_hub.relative_cost = 0
    work_hub.true_cost = 0

    available = []
    t = 0
    while work_hub.name is not end:
        work_hub.visited = True
        for elt in work_hub.links:
            current = Dijkstra_Node(map[elt].name, map[elt].cost, map[elt].links["links"])
            if (
                current.relative_cost
                > work_hub.relative_cost + current.true_cost
            ):
                current.relative_cost = (
                    work_hub.relative_cost + current.true_cost
                )
                current.origin = work_hub
                available.append(current)
        if (
            len(
                [
                    x
                    for x in available
                    if x.origin is not None and x.visited is False #add for next t of x is not at max usage
                ]
            )
            == 0
        ): #to do here the choice of node depending on the time
        # must allow to stay on itself node len is 0
            raise ValueError("No path found")
        work_hub = min(
            [
                x
                for x in available
                if x.origin is not None and x.visited is False #add for next t if not at max usage
            ],
            key=lambda s: s.relative_cost,
        )
        t += 1

    output = []
    #to add here the reservation table
    print(work_hub.name)
    #to add a while until start == None
    # then add each node if available depending time
    output = output[::-1]
    return output
