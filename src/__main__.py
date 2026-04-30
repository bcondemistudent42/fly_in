
from .display import Displayer
from .parsing.parser import Hubs, make_displayable


def find_start_end(map):
    start = "".join(
        [
            x.name
            for x in map.values()
            if isinstance(x, Hubs) and x.start is True
        ]
    )
    end = "".join(
        [x.name for x in map.values() if isinstance(x, Hubs) and x.end is True]
    )
    return (start, end)


# def get_maps():
# output = []
# for x in os.listdir("maps"):
# if x.endswith(".txt"):
# output.append(x)
# else:
# raise ValueError("Map must be a .txt")
# return output
#
# def test_maps():
# for choosen_map in get_maps():
# map = make_displayable(choosen_map)
# print(choosen_map)
# start, end = find_start_end(map)
# if (map[start].max_drone < map["nb_drones"] or
# map[end].max_drone < map["nb_drones"]):
# raise ValueError(
# f"START and END must have at least {map['nb_drones']} max drones")


def main():

    choosen_map = "03_ultimate_challenge.txt"
    map = make_displayable(choosen_map)
    start, end = find_start_end(map)
    if (
        map[start].max_drone < map["nb_drones"]
        or map[end].max_drone < map["nb_drones"]
    ):
        raise ValueError(
            f"START and END must have at least {map['nb_drones']} max drones"
        )
    display = Displayer()
    display.to_screen(map)


    # hubs = [x for x in map.values() if isinstance(x, Hubs)]
    # for i in range(len(hubs)):
    #     print()
    #     print(hubs[i].name)
    #     print(hubs[i].max_drone)


if __name__ == "__main__":
    # try:
        main()
    # except BaseException as e:
        # print(e)

# to see how to choose the map, with or without display
# within display maybe choose all available maps

# to make parsing tested by mbichet

# to handle correctly when hubs are outside the zone
