
class Dijkstra_Node:
    def __init__(self, name, cost, max_dispo, adjacent_hubs):
        self.visited = False
        self.name = name
        self.true_cost = cost
        self.relative_cost = float("inf")
        self.origin = None
        self.links = adjacent_hubs
        self.max_dispo = max_dispo


def dijkstra_init(map, start, end, work_hub, reserved):

    available = []
    t = 0
    while work_hub.name is not end:
        work_hub.visited = True
        print(work_hub.name, t)
        for elt in work_hub.links:
            current = Dijkstra_Node(map[elt].name, map[elt].cost, map[start].max_drone, map[elt].links["links"])
            if (
                current.relative_cost
                > work_hub.relative_cost + current.true_cost
            ):
                current.relative_cost = (
                    work_hub.relative_cost + current.true_cost
                )
            reserved[work_hub.name].append(t) # to init at the end
            check = False
            for elt in available:
                if elt.name == current.name:
                    check = True
            if check is False:
                available.append(current)
            if reserved.get(current.name) is None:
                reserved[current.name] = []
            current.origin = work_hub
        if (
            len(
                [
                    x
                    for x in available
                    if x.origin is not None and x.visited is False and reserved[x.name].count(t) == 0
                ]
            )
            == 0
        ):
            work_hub.relative_cost += 1
        else:
            work_hub = min(
                [
                    x
                    for x in available
                    if x.origin is not None and x.visited is False and reserved[x.name].count(t) == 0
                ],
                key=lambda s: s.relative_cost,
                )
        [print(reserved[x.name]) for x in available if x.origin is not None and x.visited is False and reserved[x.name].count(t) == 0]
        t += 1
    return reserved