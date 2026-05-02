
class Drone:
    def __init__(self, my_map, start):
        self.coord = (my_map[start].x, my_map[start].y)
        self.host_hub = start
        self.next = self.coord
