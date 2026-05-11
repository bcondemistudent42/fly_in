from .parsing.parsing_class import Hubs
from dataclasses import dataclass


@dataclass
class WorkHub:
    hub: Hubs
    timestamp: int

# WorkHub(work_hub, 0)


class Dijkstra_Node:
    def __init__(self, name, cost, adjacent_hubs):
        self.visited = False
        self.name = name
        self.true_cost = cost
        self.relative_cost = float("inf")
        self.origin = None
        self.links = adjacent_hubs


def dijkstra_init(map, start, end, reserved):

    work_hub = Dijkstra_Node(
        map[start].name, map[start].cost, map[start].links["links"]
    )
    work_hub.visited = True
    work_hub.relative_cost = 0
    work_hub.true_cost = 0
    work_hub = (work_hub, 0)

    available = []
    while work_hub[0].name is not end:
        work_hub[0].visited = True
        for elt in work_hub[0].links:
            current = Dijkstra_Node(
                map[elt].name, map[elt].cost, map[elt].links["links"]
            )
            if (
                current.relative_cost
                > work_hub[0].relative_cost + current.true_cost and work_hub[0].name != start
            ):
                current.relative_cost = (
                    work_hub[0].relative_cost + current.true_cost
                )
            current.origin = (work_hub[0], work_hub[1] + 1)
            available.append((current, work_hub[1] + 1))
        check = [
            x
            for x in available
            if x[0].origin is not None
            and x[0].visited is False
            and reserved.count((x[0].name, x[1])) < map[x[0].name].max_drone
            # and reserved.count((x[0].name, x[1]))
            # < map[x[0].name].links["max_links"]
        ]
        if len(check) == 0:
            work_hub[0].relative_cost += 1
            check.append(work_hub)
        work_hub = min(
            [x for x in check],
            key=lambda s: s[0].relative_cost,
        )

    # to add a while until start == None
    # then add each node if available depending time
    # print(output)
    reserv_table = do_reservation(work_hub, start, reserved)
    drone_path = do_path(work_hub, start)
    # print(drone_path)
    # print("reserv table ==", reserv_table)
    # print()
    return reserv_table, drone_path


def do_path(work_hub, start):
    output = []
    while work_hub[0].name != start:
        output.append((work_hub[0].name, work_hub[1]))
        work_hub = work_hub[0].origin[0]
        # print(work_hub)
    # print(output)
    return output


def do_reservation(work_hub, start, reserved):
    print(work_hub[0].name)
    while work_hub[0].name != start:
        work_hub = work_hub[0].origin[0]
        print(work_hub.name)
        reserved.append((work_hub[0].name, work_hub[1]))
    return reserved
