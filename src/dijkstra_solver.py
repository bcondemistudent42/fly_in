from .parsing.parsing_class import Hubs


class Dijkstra_Node:
    def __init__(self, name, cost, adjacent_hubs):
        self.visited = False
        self.name = name
        self.true_cost = cost
        self.relative_cost = float("inf")
        self.origin = None
        self.links = adjacent_hubs


def dijkstra_init(map, start, end):
    hub_dijstra = {}
    hub_dijstra[start] = (Dijkstra_Node(map[start].name, map[start].cost, map[start].links["links"]), 0)
    hub_dijstra[start][0].visited = True
    hub_dijstra[start][0].relative_cost = 0
    hub_dijstra[start][0].true_cost = 0

    work_hub = hub_dijstra[start][0]
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
                current.origin = (work_hub, t)
                available.append(current)
        if (
            len(
                [
                    x
                    for x in available
                    if x.origin is not None and x.visited is False and #add for next t of x is not at max usage
                ]
            )
            == 0
        ):
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

    print()
    output = []
    for elt in available:
        if elt.name == end:
            current_last = elt
            output.append(current_last.name)
            current_last = current_last.origin
            while current_last[0].name != start:
                output.append(current_last[0].name)
                current_last = current_last[0].origin
    output = output[::-1]
    return output
