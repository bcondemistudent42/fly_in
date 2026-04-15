import os

class HUB


# to do a class hub to initiatilize, with a list of connection as a list
# do attributes start and end


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
        my_start_end_hub["start_hub"] = {}
        my_dict = {}
        format_error = "Format Error: Must respect pattern 'nb_drones: int'"
        i = 0
        for line in f:
            if line.startswith("#") or len(line.strip()) == 0:
                pass
            elif ":" not in line:
                raise ValueError(format_error)
            else:
                if i == 0 and "nb_drones" not in line:
                    raise ValueError("First line must be 'nb_drones'")
                elif i == 0:
                    temp = line.split(":")
                    int(temp[1])
                    if temp[0] != "nb_drones":
                        raise ValueError(format_error)
                    else:
                        my_dict["nb_drones"] = int(temp[1])
                        print(my_dict)
                else:
                    temp = line.split(":")
                    if temp[0] == "start_hub":
                        if my_dict["start_hub"] != {}:
                            raise ValueError("Cannot init twice start_hub")
                        
                i = 1



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