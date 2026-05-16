import argparse
import os

from .dijkstra_solver import convert_to_connection
from .display import Displayer
from .drone import Drone
from .utils_main import setup_and_validate_map, assign_connections_weight

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame  # noqa: E402

from .dijkstra_solver import Graph


def main():

    parser = argparse.ArgumentParser(
        prog="Fly_In",
    )
    parser.add_argument(
        "--drone",
        default="bitcoin.png",
        required=False,
        help="Change the representation of the drones with a picture",
    )
    args = parser.parse_args()
    drone = args.drone

    my_map, start, end = setup_and_validate_map(drone)

    connections = convert_to_connection(my_map)

    assign_connections_weight(my_map, connections)

    # Compute paths for each drone (reservation-aware)
    g = Graph(my_map)
    g.dijkstra_init(my_map, start, end)
    distances = []
    paths = []
    for _ in range(my_map["nb_drones"]):
        g.do_reservation(distances)
        distances, path = g.shortest_distances()
        paths.append(path)
        # print(path)

    # Initialize display (this scales hub coordinates on my_map)
    display = Displayer(my_map, drone)
    display.reset()
    display.draw_hubs()
    pygame.display.flip()

    # Create drones after display so coordinates are scaled
    drones = [Drone(my_map, start) for _ in range(my_map["nb_drones"])]

    # Assign computed paths and initialize per-drone pointers
    for drone, path in zip(drones, paths):
        drone.path = path
        drone.path_index = 0
        # place drone at the visual center of the start hub
        sx = my_map[start].x + (display.size - display.drone_img.get_width()) / 2
        sy = my_map[start].y + (display.size - display.drone_img.get_height()) / 2
        drone.coord = (sx, sy)

    # Debug: print start/hub coordinates
    # for i, drone in enumerate(drones):
        # print(f"Drone {i} coord={drone.coord} | start_hub=({my_map[start].x},{my_map[start].y})")

    # Show all drones at their starting positions once
    display.display_drones([(int(drone.coord[0]), int(drone.coord[1])) for drone in drones], drones)
    pygame.display.flip()

    # Keep the window visible briefly so the start positions are seen
    tmp_clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_ticks < 200:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                pygame.quit()
                return
        tmp_clock.tick(60)

    # Determine global time horizon
    max_time = 0
    for p in paths:
        for _, t in p:
            if t > max_time:
                max_time = t

    clock = pygame.time.Clock()

    def bfs_path(start_hub, goal_hub, my_map):
        # simple BFS to return list of hub names from start to goal (inclusive)
        from collections import deque

        q = deque([start_hub])
        prev = {start_hub: None}
        while q:
            cur = q.popleft()
            if cur == goal_hub:
                break
            for nb in my_map[cur].links["links"]:
                if nb not in prev:
                    prev[nb] = cur
                    q.append(nb)

        if goal_hub not in prev:
            return None
        # rebuild path
        path = []
        cur = goal_hub
        while cur is not None:
            path.append(cur)
            cur = prev[cur]
        return path[::-1]

    # Animate until all drones have exhausted their planned paths
    current_time = 0
    while True:
        # redraw every frame so hover info is instant
        display.display_drones([(int(d.coord[0]), int(d.coord[1])) for d in drones], drones)
        pygame.display.flip()

        # collect drones that must move at this time
        to_move = []
        for drone in drones:
            # advance pointer until we find current or future time
            while drone.path_index < len(drone.path) and drone.path[drone.path_index][1] < current_time:
                drone.path_index += 1
            if drone.path_index < len(drone.path) and drone.path[drone.path_index][1] == current_time:
                hub_name, _t = drone.path[drone.path_index]
                # compute visual center for the hub or step-by-step if not adjacent
                current_host = getattr(drone, "host_hub", start)
                if hub_name not in my_map[current_host].links["links"]:
                    # not adjacent -> find intermediate path via BFS
                    route = bfs_path(current_host, hub_name, my_map)
                    if route is None:
                        print(f"Warning: no route found between {current_host} and {hub_name}")
                        # fallback: jump directly
                        target = hub_name
                    else:
                        # take next hop
                        if len(route) >= 2:
                            target = route[1]
                        else:
                            target = hub_name
                    nx = my_map[target].x + (display.size - display.drone_img.get_width()) / 2
                    ny = my_map[target].y + (display.size - display.drone_img.get_height()) / 2
                else:
                    nx = my_map[hub_name].x + (display.size - display.drone_img.get_width()) / 2
                    ny = my_map[hub_name].y + (display.size - display.drone_img.get_height()) / 2

                drone.next = (nx, ny)
                to_move.append(drone)
                drone.path_index += 1

        # move scheduled drones (draw non-moving drones in place so they remain visible)
        if to_move:
            for d in drones:
                if d not in to_move:
                    d.next = d.coord
            display.move_drones(drones, clock, pause_ms=400)

        # keep app responsive during idle ticks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                pygame.quit()
                return

        # stop when no drone has remaining scheduled hops
        pending = any(drone.path_index < len(drone.path) for drone in drones)
        if not pending and not to_move:
            break

        current_time += 1
        clock.tick(60)



if __name__ == "__main__":
    # try:
    main()
# except BaseException as e:
# print(e)


# URGENT GERER LEX MAX LINKS PROPREMENT

# to handle when fisrt connection after start have max drone at 0
# to handle when max_links < max_capacity dron still goiing but should not


# to handle hedge case 

# Medium Level 2: Circular loop with restricted zones
# nb_drones: 6

# start_hub: start 0 0 [color=green max_drones=6]
# hub: loop_a 1 0 [color=black max_drones=0]
# hub: loop_b 2 0 [color=orange max_drones=2]
# hub: loop_c 2 1 [color=orange max_drones=2]
# hub: loop_d 1 1 [color=orange max_drones=2]
# hub: exit_point 3 0 [zone=restricted color=blue]
# end_hub: goal 4 0 [color=red max_drones=6]

# connection: start-loop_a [max_link_capacity=2]
# connection: loop_a-loop_b [max_link_capacity=2]
# connection: loop_b-loop_c [max_link_capacity=2]
# connection: loop_c-loop_d [max_link_capacity=2]
# connection: loop_d-loop_a [max_link_capacity=2]
# connection: loop_b-exit_point
# connection: exit_point-goal
