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
                hub_dijstra[elt.name] = Dijkstra_Node(elt.name, elt.cost, elt.links["links"])
                hub_dijstra[elt.name].visited = True
                hub_dijstra[elt.name].cost = 0
            else:
                hub_dijstra[elt.name] = Dijkstra_Node(elt.name, elt.cost, elt.links["links"])
    
    work_hub = [x for x in hub_dijstra.values() if x.visited is True][0]
    while work_hub.name != end and len([x for x in hub_dijstra.values() if x.visited is False]) != 0 :
        work_hub.visited = True
        available = [x for x in hub_dijstra.values() if x.visited is False]
        if len(available) == 0: #here to add an if no links else choose the other min 
            print("We have a problem in dijsktra no available hubs")
            return
        nxt_min = min(available, key=lambda s: s.true_cost)
        hub_dijstra[nxt_min.name].origin = work_hub
        if hub_dijstra[nxt_min.name].relative_cost > work_hub.relative_cost:
            hub_dijstra[nxt_min.name].relative_cost += work_hub.relative_cost
        work_hub = hub_dijstra[nxt_min.name]

    actual = hub_dijstra[end]
    test = []
    while(actual.name != "start"):
        test.append(actual.name)
        actual = actual.origin
    test = test[::-1]
    return test

# to handle issues, the thing is that i am not looking in links but in all





