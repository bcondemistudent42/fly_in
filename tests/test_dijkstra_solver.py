import os
import unittest

from src.dijkstra_solver import Graph, convert_to_connection
from src.parsing.parser import make_displayable
from src.parsing.parsing_class import Hubs
from src.utils_main import assign_connections_weight


def find_start_end(current_map):
    start = next(x.name for x in current_map.values() if isinstance(x, Hubs) and x.start)
    end = next(x.name for x in current_map.values() if isinstance(x, Hubs) and x.end)
    return start, end


class DijkstraReservationRegressionTest(unittest.TestCase):
    def test_solver_handles_all_packaged_maps(self):
        map_files = sorted(x for x in os.listdir("maps") if x.endswith(".txt"))
        for map_file in map_files:
            with self.subTest(map_file=map_file):
                current_map = make_displayable(map_file)
                start, end = find_start_end(current_map)
                connections = convert_to_connection(current_map)
                assign_connections_weight(current_map, connections)

                graph = Graph(current_map)
                graph.dijkstra_init(current_map, start, end)

                for _ in range(current_map["nb_drones"]):
                    path = graph.shortest_distances()
                    self.assertTrue(path)
                    self.assertEqual(path[0][1], start)
                    self.assertEqual(path[-1][1], end)
                    graph.do_reservation(path)


if __name__ == "__main__":
    unittest.main()
