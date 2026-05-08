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
    work_hub = (work_hub, 0)

    available = []
    print("reserved ==", reserved)
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
        check = [ x for x in available if x[0].origin is not None and x[0].visited is False and (x[0].name, x[1]) not in reserved]#add for next t of x is not at max usage
        check1 = [ (x[0].name, x[1]) for x in available if x[0].origin is not None and x[0].visited is False and (x[0].name, x[1]) not in reserved]#add for next t of x is not at max usage
        print(check1)
        if (len(check) == 0): #to do here the choice of node depending on the time
            work_hub[0].relative_cost += 1 # must allow to stay on itself node len is 0
            check.append(work_hub)
            print("giga caca", work_hub[0].name)
        work_hub = min(
            [ x for x in check],
            key=lambda s: s[0].relative_cost,
        )
        t += 1

   #to add a while until start == None
    # then add each node if available depending time
    # print(output)
    print()
    print()
    rslt = do_reservation(work_hub, start, reserved, available, end)
    print(rslt)
    return rslt

def do_reservation(work_hub, start, reserved, available, end):
    while work_hub[0].name != start:
        work_hub = work_hub[0].origin[0]
        reserved.add(tuple((work_hub[0].name, work_hub[1])))

    return reserved