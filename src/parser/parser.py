import os


class Hubs:
    def __init__(
                 self,
                 name: str,
                 x: int,
                 y: int,
                #  color: str,
                #  zone_type: str
                 ):
        self.name = name
        self.x = int(x)
        self.y = int(y)
        # to add some chekc for zone wtype and colors and list of connections
        # to add colors, zone type by default and list of connections


def get_maps() -> list | None:
    output = []
    for x in os.listdir("maps"):
        if x.endswith(".txt"):
            output.append(x)
        else:
            raise ValueError("Map must be a .txt")
    return output


def map_valid(my_map):
    with open("maps/" + my_map) as f:
        my_hubs = {}
        my_hubs["start_hub"] = {}
        my_hubs["end_hub"] = {}
        format_error = "Format Error: Must respect pattern 'nb_drones: int'"
        i = 0
        j = 1
        for line in f:
            if line.startswith("#") or len(line.strip()) == 0:
                pass
            elif ":" not in line:
                raise ValueError(format_error + f"Line: {j}")
            else:
                if i == 0 and "nb_drones" not in line:
                    raise ValueError(f"First line must be 'nb_drones', Line: {j}")
                elif i == 0:
                    temp = line.split(":")
                    int(temp[1])
                    if temp[0] != "nb_drones":
                        raise ValueError(format_error + f"Line: {j}")
                    else:
                        my_hubs["nb_drones"] = int(temp[1])
                else:
                    key = line.split(":")
                    data = key[1].split()
                    if key[0] == "start_hub":
                        if my_hubs["start_hub"] != {}:
                            raise ValueError("Can't init twice start,"
                                             f"Line: {j}")
                        my_hubs["start_hub"] = Hubs(data[0], data[1], data[2]) #a voir pour les couleurs 
                    elif key[0] == "end_hub":
                        if my_hubs["end_hub"] != {}:
                            raise ValueError(f"Cannot init twice end_hub, Line: {j}")
                        my_hubs["end_hub"] = Hubs(data[0], data[1], data[2])
                    elif key[0] == "hub":
                        my_hubs[data[0]] = Hubs(data[0], data[1], data[2])
                    else:
                        raise ValueError(f"Unknown Type, {format_error}, Line: {j}")

# to do later the connections stuff to handle
                i = 1
            j += 1
    for elt in my_hubs.values():
        try:
            print(elt.name)
        except Exception:
            pass


def main():
    try:
        maps = get_maps()
        if len(maps) == 0:
            raise ValueError("At least one map must be available")
    except ValueError as e:
        print(f"File error: {e}")
        return
    except Exception as e:
        print(f"Caught Error : {e}")
        return
    try:
        for elt in maps:
            map_valid(elt)
    except ValueError as e:
        print(e)
        return
    except BaseException as e:
        print(e)
        return


if __name__ == "__main__":
    main()


# to add try except for main at the end