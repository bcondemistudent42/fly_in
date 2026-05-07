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
                if x.origin is not None and x.visited is False
            ],
            key=lambda s: s.relative_cost,
        )
        table = create_table(work_hub, start, reserved, available)
        print(f"table == {table}")
        print(f"reserved == {reserved}")

   #to add a while until start == None
    # then add each node if available depending time
    # print(output)
    print()
    print()
    rslt = create_table(work_hub, start, reserved, available)
    print(rslt)
    return rslt

def create_table(work_hub, start, reserved, available):
    temp = []
    while work_hub.name != start:
        temp.append(work_hub.name)
        work_hub = work_hub.origin
    #to do here, the minimum thin ect if the node is in reserved
    output = []
    temp = temp[::-1]
    i = 1
    for elt in temp:
        output.append((elt, i))
        i += 1
    
    for work_hub_bis in output:
        if work_hub_bis in reserved:
            temp = [x for x in available if x.origin is not None and x.visited is False]
            temp.append(work_hub)
            work_hub.relative_cost += 1
            new_work_hub = min(temp, key=lambda s: s.relative_cost)
            if new_work_hub == work_hub:
                # find a system to pass to the next t = time
            else:
                # just choose another hub
            break
            # i have to take the minimum after added +1 to relative cost of tha actual 
            # and puted it in available
            # I MUST HANDLE THE TIME THING TO PUT IT TO THE NEXT t
            # to see the logic behind, or pass and somewhere else or stay

    return output