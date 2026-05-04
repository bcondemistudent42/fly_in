from .parsing.parsing_class import Hubs


class Dijkstra_Node:
    def __init__(self, name, cost, adjacent_hubs):
        self.visited = False
        self.name = name
        self.true_cost = cost
        self.relative_cost = float("inf")
        self.origin = None
        self.links = adjacent_hubs


def dijkstra_init(my_map, start, end):
    hub_dijstra = {}
    for elt in my_map.values():
        if isinstance(elt, Hubs):
            if elt.name == start:
                hub_dijstra[elt.name] = Dijkstra_Node(
                    elt.name, elt.cost, elt.links["links"]
                )
                hub_dijstra[elt.name].visited = True
                hub_dijstra[elt.name].relative_cost = 0
                hub_dijstra[elt.name].true_cost = 0
            else:
                hub_dijstra[elt.name] = Dijkstra_Node(
                    elt.name, elt.cost, elt.links["links"]
                )

    work_hub = [x for x in hub_dijstra.values() if x.visited is True][0]
    while hub_dijstra[end].origin is None:
        work_hub.visited = True
        for elt in work_hub.links:
            if (
                hub_dijstra[elt].relative_cost
                > work_hub.relative_cost + hub_dijstra[elt].true_cost
            ):
                hub_dijstra[elt].relative_cost = (
                    work_hub.relative_cost + hub_dijstra[elt].true_cost
                )
                hub_dijstra[elt].origin = work_hub
        if (
            len(
                [
                    x
                    for x in hub_dijstra.values()
                    if x.origin is not None and x.visited is False
                ]
            )
            == 0
        ):
            raise ValueError("No path found")
        work_hub = min(
            [
                x
                for x in hub_dijstra.values()
                if x.origin is not None and x.visited is False
            ],
            key=lambda s: s.relative_cost,
        )

    actual = hub_dijstra[end]
    test = []
    while actual.origin is not None:
        if actual.name is not None:
            print(actual.name)
            test.append(actual.name)
        actual = actual.origin
    test = test[::-1]
    print(test)
    return test
