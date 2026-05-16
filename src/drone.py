
class Drone:
    def __init__(self, my_map, start):
        self.coord = (my_map[start].x, my_map[start].y)
        self.host_hub = start
        self.path = []
        self.path_index = 0
        self.next = self.coord

# to change later can't have one class in a emtpy file
