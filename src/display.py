import os

from .parsing.parsing_class import Hubs

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame  # noqa: E402


class Displayer:
    def __init__(self, my_map, drone_img) -> None:
        pygame.init()
        pygame.font.init()
        info = pygame.display.Info()

        width, height = 3 * (info.current_w / 4), 3 * (info.current_h / 4)
        self.screen = pygame.display.set_mode((width, height))

        self.width = width
        self.height = height
        self.my_map = my_map
        self.size = 50
        self.padding = self.size / 2

        x_max = max([x.x for x in self.my_map.values() if isinstance(x, Hubs)])
        x_min = min([x.x for x in self.my_map.values() if isinstance(x, Hubs)])
        y_max = max([x.y for x in self.my_map.values() if isinstance(x, Hubs)])
        y_min = min([x.y for x in self.my_map.values() if isinstance(x, Hubs)])

        self.drone_img = pygame.transform.scale(
            pygame.image.load("visual_drones/" + drone_img).convert_alpha(),
            (45, 45),
        )
        self.font = pygame.font.SysFont(None, 20)
        self.drones = []

        self.math_utils(x_max, x_min, y_max, y_min)
        for elt in my_map.values():
            if isinstance(elt, Hubs):
                elt.x = int((elt.x - x_min) * (self.scale) + self.offset_x)
                elt.y = int((elt.y - y_min) * (self.scale) + self.offset_y)

        pygame.display.set_caption("Fly-in")

    def reset(self):
        self.screen.fill((105, 135, 138))

    def draw_lines(self, my_map, key, elt):
        for elt1 in my_map[key].links["links"]:
            pygame.draw.line(
                self.screen,
                "black",
                (
                    my_map[elt1].x + (self.size / 2),
                    my_map[elt1].y + (self.size / 2),
                ),
                (
                    (elt.x + (self.size / 2)),
                    (elt.y + (self.size / 2)),
                ),
                5,
            )

    def draw_one_hub(self, elt):
        pygame.draw.rect(
            self.screen,
            elt.color,
            (
                elt.x,
                elt.y,
                self.size,
                self.size,
            ),
        )

    def math_utils(self, x_max, x_min, y_max, y_min):
        temp_x = max(1, x_max - x_min)
        temp_y = max(1, y_max - y_min)

        scale_x = (self.width - (self.padding * 2) - self.size) / temp_x
        scale_y = (self.height - (self.padding * 2) - self.size) / temp_y
        scale = min(scale_x, scale_y)

        graph_width = (temp_x * scale) + self.size
        graph_height = (temp_y * scale) + self.size

        offset_x = (self.width - graph_width) / 2
        offset_y = (self.height - graph_height) / 2

        self.offset_x = offset_x
        self.offset_y = offset_y

        self.scale = scale

    def draw_hubs(self):
        if self.my_map is None:
            raise ValueError("Map Error")

        for key, elt in self.my_map.items():
            try:
                if isinstance(elt, Hubs):
                    self.draw_one_hub(elt)
                    self.draw_lines(self.my_map, key, elt)
            except ValueError:
                raise ValueError(f"This is not a color: '{elt.color}'")

    def display_drones(self, drones_positions, drones_list):
        self.reset()
        self.draw_hubs()
        for pos in drones_positions:
            # ensure integer pixel positions when blitting
            x = int(pos[0])
            y = int(pos[1])
            self.screen.blit(self.drone_img, (x, y))

        mx, my = pygame.mouse.get_pos()
        for key, elt in self.my_map.items():
            if isinstance(elt, Hubs):
                hx, hy = elt.x, elt.y
                if hx <= mx <= hx + self.size and hy <= my <= hy + self.size:
                    # count drones whose host_hub matches this key
                    count = sum(1 for d in drones_list if getattr(d, "host_hub", None) == key)
                    max_count = getattr(elt, "max_drone", None)

                    cur_surf = self.font.render(str(count), True, (0, 150, 0))
                    if max_count is None:
                        max_surf = self.font.render("/", True, (0, 0, 0))
                    else:
                        max_surf = self.font.render(f"/{max_count}", True, (0, 0, 0))

                    # background rect to improve readability
                    total_width = cur_surf.get_width() + max_surf.get_width()
                    rect = pygame.Rect(hx + self.size + 4, hy, total_width, max(cur_surf.get_height(), max_surf.get_height()))
                    pygame.draw.rect(self.screen, (255, 255, 255), rect)
                    # blit current then suffix
                    self.screen.blit(cur_surf, rect.topleft)
                    self.screen.blit(max_surf, (rect.left + cur_surf.get_width(), rect.top))
                    break

    def move_drones(self, drones, the_clock, pause_ms: int = 400):
        positions = [pygame.Vector2(drone.coord) for drone in drones]
        destinations = [pygame.Vector2(drone.next) for drone in drones]

        distances = [
            positions[i].distance_to(destinations[i])
            for i in range(len(drones))
        ]
        directions = []
        for i in range(len(drones)):
            if distances[i] > 0:
                directions.append((destinations[i] - positions[i]).normalize())
            else:
                directions.append(pygame.Vector2(0, 0))

        vitesse = 4
        while (
            max(
                pos.distance_to(dest)
                for pos, dest in zip(positions, destinations)
            )
            > vitesse
        ):
            for i in range(len(drones)):
                if positions[i].distance_to(destinations[i]) > vitesse:
                    positions[i] += directions[i] * vitesse

            self.display_drones([pos for pos in positions], drones)
            pygame.display.flip()
            the_clock.tick(60)

        self.display_drones([dest for dest in destinations], drones)
        pygame.display.flip()

        for i, drone in enumerate(drones):
            drone.coord = (destinations[i].x, destinations[i].y)
            # assign host_hub when a drone arrives inside a hub rectangle
            for key, elt in self.my_map.items():
                if isinstance(elt, Hubs):
                    hx, hy = elt.x, elt.y
                    if hx <= drone.coord[0] <= hx + self.size and hy <= drone.coord[1] <= hy + self.size:
                        drone.host_hub = key
                        break

        # small pause after arrival so the user can see drones on the hub
        start_ticks = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_ticks < pause_ms:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                    pygame.quit()
                    return
            # redraw to keep hover info responsive
            self.display_drones([dest for dest in destinations], drones)
            pygame.display.flip()
            the_clock.tick(60)
