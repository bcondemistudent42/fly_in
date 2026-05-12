from dataclasses import dataclass
from .parsing.parsing_class import Hubs

# WorkHub(work_hub, 0)


class Dijkstra_Node:
    def __init__(self, name, cost, adjacent_hubs):
        self.visited = False
        self.name = name
        self.true_cost = cost
        self.relative_cost = float("inf")
        self.origin = None
        self.links = adjacent_hubs

@dataclass
class WorkHub:
    hub: Dijkstra_Node
    time: int

def dijkstra_init(map, start, end, reserved):

    print("reserved ==", reserved)
    available = []
    nodes = {
    hub.name: Dijkstra_Node(hub.name, hub.cost, hub.links["links"])
        for hub in map.values()
            if isinstance(hub, Hubs)
    }

    nodes[start].visited = True
    nodes[start].relative_cost = 0
    nodes[start].true_cost = 0

    work_hub = WorkHub(nodes[start], 0)

    while work_hub.hub.name != end:
        work_hub.hub.visited = True
        right_time = work_hub.time + 1
        for elt in work_hub.hub.links:
            current = nodes[elt]
            if (
                current.relative_cost
                > work_hub.hub.relative_cost + current.true_cost
            ):
                current.relative_cost = (
                    work_hub.hub.relative_cost + current.true_cost
                )
                current.origin = WorkHub(work_hub.hub, right_time)
            available.append(WorkHub(current, right_time))
        check = [
            x
            for x in available
            if x.hub.origin is not None
            and x.hub.visited is False
            and reserved.count((x.hub.name, x.time + 1)) < map[x.hub.name].max_drone
            # and reserved.count((x[0].name, x[1]))
            # < map[x[0].name].links["max_links"]
        ]
        if len(check) == 0:
            work_hub.hub.relative_cost += 1
            work_hub.time += 1
            check.append(work_hub)
        work_hub = min(
            [x for x in check],
            key=lambda s: s.hub.relative_cost,
        )

    work_hub.time += 1

    reserv_table = do_reservation(work_hub, start, end, reserved)
    drone_path = do_path(work_hub, start)
    print(drone_path)
    print()
    print()
    return reserv_table, drone_path


def do_path(work_hub, start):
    output = []
    while work_hub.hub.name != start:
        output.append((work_hub.hub.name, work_hub.time))
        work_hub = work_hub.hub.origin
    return output


def do_reservation(work_hub, start, end, reserved):
    while work_hub.hub.name != start:
        work_hub = work_hub.hub.origin
        if work_hub.hub.name != start and work_hub.hub.name != end:
            reserved.append((work_hub.hub.name, work_hub.time))
    return reserved
