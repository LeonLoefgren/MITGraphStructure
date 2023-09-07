
#
# Pathfinder for digraphs with two weight-parameters per edge.
#
from graph_1 import Digraph, Node, WeightedEdge
test_map_filename = "testing_graph.txt"

def load_map(map_filename):
    """
    Parses the map file and constructs a directed graph

    Parameters:
        map_filename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a Digraph representing the map
    """
    digraph_mit = Digraph()
    file = open(map_filename, "r", encoding="utf-8")
    list = []
    for line in file:
        nest_list = []
        for data in line.split(" "):
            nest_list.append(data.strip("\n"))
        list.append(nest_list)
    file.close()
    for data in list:
        src = Node(data[0])
        dest = Node(data[1])
        if not digraph_mit.has_node(src):
            digraph_mit.add_node(src)
        if not digraph_mit.has_node(dest):
            digraph_mit.add_node(dest)
        digraph_mit.add_edge(WeightedEdge(src, dest, int(data[2]), int(data[3])))
    return digraph_mit

def get_node_object(digraph, name):
    """
    Returns the node (object) with the specified name.
    :param digraph: The digraph in question.
    :param name: The name (string) of the node.
    :return: The node (object).
    """
    for node in digraph.edges:
        if node.get_name() == name:
            return node

def distance_sum(digraph, path):
    """
    Calculates the total distance and outdoor distance for a certain path.
    :param digraph: The digraph in question.
    :param path: The path in question.
    :return: Returns a tuple (total distance, outdoor distance).
    """
    total_distance = 0
    outdoor_distance = 0
    for node in path:
        try:
            for edge in digraph.edges[get_node_object(digraph, node)]:
                if edge.get_destination().get_name() == path[path.index(node) + 1]:
                    total_distance += edge.get_total_distance()
                    outdoor_distance += edge.get_outdoor_distance()
        except IndexError:
            pass
    return total_distance, outdoor_distance

def generate_paths(digraph, start, end, path = None):
    """
    Uses DFS to generate all possible paths from a start node to an end node.
    :param digraph: The digraph in question.
    :param start: The starting node.
    :param end: The end node.
    :param path: Recursive parameter. Default is None.
    :return: Yields all possible paths together with their total distance and outdoor distance:
                ([path], (total distance, outdoor distance))
    """
    if path == None:
        path = [start]
    if start == end:
        yield (path, distance_sum(digraph, path))
    for edge in digraph.edges[get_node_object(digraph, start)]:
        if edge.get_destination().get_name() not in path:
            yield from generate_paths(digraph, edge.get_destination().get_name(), end,
                                      path + [edge.get_destination().get_name()])

def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    """
    Finds the shortest path from start to end using a directed depth-first
    search. The total distance traveled on the path must not
    exceed max_total_dist, and the distance spent outdoors on this path must
    not exceed max_dist_outdoors.

    Parameters:
        digraph: Digraph instance
            The graph on which to carry out the search
        start: string
            Building number at which to start
        end: string
            Building number at which to end
        max_total_dist: int
            Maximum total distance on a path
        max_dist_outdoors: int
            Maximum distance spent outdoors on a path

    Returns:
        The shortest-path from start to end, represented by
        a list of building numbers (in strings), [n_1, n_2, ..., n_k],
        where there exists an edge from n_i to n_(i+1) in digraph,
        for all 1 <= i < k

        If there exists no path that satisfies max_total_dist and
        max_dist_outdoors constraints, then raises a ValueError.
    """
    if (not digraph.has_node(get_node_object(digraph, start))) and \
            (not digraph.has_node(get_node_object(digraph, end))):
        raise ValueError("Startnode or Endnode does not exist in this graph.")
        return None
    possible_paths = list(generate_paths(digraph, start, end))
    for path in possible_paths.copy():
        if path[1][0] > max_total_dist or path[1][1] > max_dist_outdoors:
            possible_paths.remove(path)
    if len(possible_paths) == 0:
        raise ValueError("No path exists under the current constraints.")
        return None
    possible_paths.sort(key= lambda x: x[1][0])
    return possible_paths[0][0]


test_graph = load_map(test_map_filename)
print(directed_dfs(test_graph, "1", "5", 100000, 10000))





# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

# class Ps2Test(unittest.TestCase):
#     LARGE_DIST = 99999
#
#     def setUp(self):
#         self.graph = load_map("mit_map.txt")
#
#     def test_load_map_basic(self):
#         self.assertTrue(isinstance(self.graph, Digraph))
#         self.assertEqual(len(self.graph.nodes), 37)
#         all_edges = []
#         for _, edges in self.graph.edges.items():
#             all_edges += edges  # edges must be dict of node -> list of edges
#         all_edges = set(all_edges)
#         self.assertEqual(len(all_edges), 129)
#
#     def _print_path_description(self, start, end, total_dist, outdoor_dist):
#         constraint = ""
#         if outdoor_dist != Ps2Test.LARGE_DIST:
#             constraint = "without walking more than {}m outdoors".format(
#                 outdoor_dist)
#         if total_dist != Ps2Test.LARGE_DIST:
#             if constraint:
#                 constraint += ' or {}m total'.format(total_dist)
#             else:
#                 constraint = "without walking more than {}m total".format(
#                     total_dist)
#
#         print("------------------------")
#         print("Shortest path from Building {} to {} {}".format(
#             start, end, constraint))
#
#     def _test_path(self,
#                    expectedPath,
#                    total_dist=LARGE_DIST,
#                    outdoor_dist=LARGE_DIST):
#         start, end = expectedPath[0], expectedPath[-1]
#         self._print_path_description(start, end, total_dist, outdoor_dist)
#         dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
#         print("Expected: ", expectedPath)
#         print("DFS: ", dfsPath)
#         self.assertEqual(expectedPath, dfsPath)
#
#     def _test_impossible_path(self,
#                               start,
#                               end,
#                               total_dist=LARGE_DIST,
#                               outdoor_dist=LARGE_DIST):
#         self._print_path_description(start, end, total_dist, outdoor_dist)
#         with self.assertRaises(ValueError):
#             directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
#
#     def test_path_one_step(self):
#         self._test_path(expectedPath=['32', '56'])
#
#     def test_path_no_outdoors(self):
#         self._test_path(
#             expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)
#
#     def test_path_multi_step(self):
#         self._test_path(expectedPath=['2', '3', '7', '9'])
#
#     def test_path_multi_step_no_outdoors(self):
#         self._test_path(
#             expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)
#
#     def test_path_multi_step2(self):
#         self._test_path(expectedPath=['1', '4', '12', '32'])
#
#     def test_path_multi_step_no_outdoors2(self):
#         self._test_path(
#             expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
#             outdoor_dist=0)
#
#     def test_impossible_path1(self):
#         self._test_impossible_path('8', '50', outdoor_dist=0)
#
#     def test_impossible_path2(self):
#         self._test_impossible_path('10', '32', total_dist=100)
#
#
# if __name__ == "__main__":
#     unittest.main()
