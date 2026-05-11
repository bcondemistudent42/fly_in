from dataclasses import dataclass




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

    work_hub = WorkHub(Dijkstra_Node(map[start].name, map[start].cost, map[start].links["links"]), 0)
    work_hub.hub.visited = True
    work_hub.hub.relative_cost = 0
    work_hub.hub.true_cost = 0

    print()
    print()
    print("reserved ==", reserved)

    available = []
    while work_hub.hub.name is not end:
        work_hub.hub.visited = True
        for elt in work_hub.hub.links:
            current = Dijkstra_Node(
                map[elt].name, map[elt].cost, map[elt].links["links"]
            )
            if (
                current.relative_cost
                > work_hub.hub.relative_cost + current.true_cost and work_hub.hub.name != start
            ):
                current.relative_cost = (
                    work_hub.hub.relative_cost + current.true_cost
                )
            current.origin = WorkHub(work_hub.hub, work_hub.time + 1)
            available.append(WorkHub(current, work_hub.time + 1))
        check = [
            x
            for x in available
            if x.hub.origin is not None
            and x.hub.visited is False
            and reserved.count((x.hub.name, x.time + 1)) < map[x.hub.name].max_drone
            # and reserved.count((x[0].name, x[1]))
            # < map[x[0].name].links["max_links"]
        ]
        # check1 = [
        # reserved.count((x.hub.name, x.time + 1))
        # for x in available
        # if x.hub.origin is not None
        # and x.hub.visited is False
        # and reserved.count((x[0].name, x[1]))
        # < map[x[0].name].links["max_links"]
        # ]
        # print(check1)
        if len(check) == 0:
            work_hub.hub.relative_cost += 1
            work_hub.time += 1
            check.append(work_hub)
        work_hub = min(
            [x for x in check],
            key=lambda s: s.hub.relative_cost,
        )

    work_hub.time += 1
    # to add a while until start == None
    # then add each node if available depending time
    # print(output)
    reserv_table = do_reservation(work_hub, start, end, reserved)
    drone_path = do_path(work_hub, start)
    print(drone_path)
    # print("reserv table ==", reserv_table)
    # print()
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
