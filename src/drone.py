
class Drone:
    def __init__(self, my_map, start, visual):
        self.coord = (my_map[start].x, my_map[start].y)
        self.host_hub = start
        self.next = self.coord
        self.visual = visual
        self.path = []

# to change later can't have one class in a emtpy file
