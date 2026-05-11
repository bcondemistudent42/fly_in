from .parsing.parsing_class import Hubs


class Dijkstra_Node:
    def __init__(self, name, cost, adjacent_hubs):
        self.visited = False
        self.name = name
        self.true_cost = cost
        self.relative_cost = float("inf")
        self.origin = None
        self.links = adjacent_hubs


def dijkstra_init(map, start, end, reserved):

    work_hub = Dijkstra_Node(map[start].name, map[start].cost, map[start].links["links"])
    work_hub.visited = True
    work_hub.relative_cost = 0
    work_hub.true_cost = 0
    work_hub = (work_hub, 0)

    available = []
    t = 1
    while work_hub[0].name is not end:
        work_hub[0].visited = True
        for elt in work_hub[0].links:
            current = Dijkstra_Node(map[elt].name, map[elt].cost, map[elt].links["links"])
            if (
                current.relative_cost
                > work_hub[0].relative_cost + current.true_cost
            ):
                current.relative_cost = (
                    work_hub[0].relative_cost + current.true_cost
                )
                current.origin = (work_hub, t)
                available.append((current, t))
        check = [x for x in available if x[0].origin is not None and x[0].visited is False and reserved.count((x[0].name, x[1])) < map[x[0].name].max_drone and reserved.count((x[0].name, x[1])) < map[x[0].name].links["max_links"]]
        check1 = [(x[0].name,reserved.count((x[0].name, x[1])), map[x[0].name].links["max_links"]) for x in available if x[0].origin is not None and x[0].visited is False and reserved.count((x[0].name, x[1])) < map[x[0].name].max_drone and reserved.count((x[0].name, x[1])) < map[x[0].name].links["max_links"]]
        print(check1)
        if (len(check) == 0):
            work_hub[0].relative_cost += 1
            check.append(work_hub)
        work_hub = min(
            [ x for x in check],
            key=lambda s: s[0].relative_cost,
        )
        t += 1

   #to add a while until start == None
    # then add each node if available depending time
    # print(output)
    reserv_table = do_reservation(work_hub, start, reserved, available, end)
    drone_path = do_path(work_hub, start)
    # print(reserv_table)
    return reserv_table, drone_path 


def do_path(work_hub, start):
    output = []
    while (work_hub[0].name != start):
        output.append((work_hub[0].name, work_hub[1]))
        work_hub = work_hub[0].origin[0]
        # print(work_hub)
    # print(output)
    return output




def do_reservation(work_hub, start, reserved, available, end):
    while work_hub[0].name != start:
        work_hub = work_hub[0].origin[0]
        reserved.append(tuple((work_hub[0].name, work_hub[1])))
    return reserved
