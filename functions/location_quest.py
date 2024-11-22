from utils import tools as t
import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
import random as r

FILEPATH = "./save/"

# just in case I need it in the future:
# https://stackoverflow.com/questions/46238813/osmnx-get-coordinates-of-nodes-using-osm-id


# noinspection SpellCheckingInspection
def request_graph(
	address: str = "Hallituskatu 1A, 96100 Rovaniemi",
	distance_covered: int = 5000,
	save: bool = True,
	save_name: str = "rovaniemi"
) -> nx.MultiDiGraph:
	"""
	Requests a graph from the API handler, also automatically saves it.
	@param address: custom center position
	@param distance_covered: distance from center position, recommended 4000 - 10_000
	@param save: should the graph be saved?
	@param save_name: what name should the graph be saved at? (automatically overwrites existing files)
	@return:
	"""
	multi_graph = ox.graph_from_address(address, dist = distance_covered, network_type = "walk")
	if save:
		ox.save_graphml(multi_graph, f"{FILEPATH}{save_name}.graphml")
	return multi_graph


def load_graph(graph_name: str = "rovaniemi") -> nx.MultiDiGraph:
	"""
	Loads graph if exists.
	Expected errors: FileNotFoundError (in case the filename doesn't exist)
	@param graph_name: the filename of the graph
	@return:
	"""
	if graph_name[:-8] == ".graphml":
		graph = ox.load_graphml(f"{FILEPATH}{graph_name}")
	else:
		graph = ox.load_graphml(f"{FILEPATH}{graph_name}.graphml")

	# basically simplifies the graph somewhat
	graph_proj = ox.project_graph(graph)
	graph = ox.consolidate_intersections(graph_proj, rebuild_graph = True, tolerance = 15, dead_ends = False)
	return graph


# noinspection SpellCheckingInspection
def get_graph(
	graph_name: str = "rovaniemi",
	address: str = "Hallituskatu 1A, 96100 Rovaniemi",
	distance: int = 5000,
	save: bool = True
) -> nx.MultiDiGraph:
	"""
	Tries to load graph, if it is not found requests one with the API
	@param graph_name: the filename of the graph to load / request
	@param address: for request: custom center position
	@param distance: for request: distance from center position, recommended 4000 - 10_000
	@param save: for request: should the graph be saved?
	@return:
	"""
	try:
		graph = load_graph(graph_name)
	except FileNotFoundError:
		graph = request_graph(address, distance, save, graph_name)

	return graph


def show_graph(graph: nx.MultiDiGraph, coords: list[t.Coord] = None) -> None:
	"""
	Displays graph, optionally with coordinate(s) marked.
	@param graph:
	@param coords: list of coordinates to display on the map (optional)
	@return:
	"""
	fig, ax = ox.plot_graph(graph, show = False, close = False)
	if coords:
		for coord in coords:
			coord.map_to_graph(ax)
	plt.show()


def _quest_recursive(graph: nx.MultiDiGraph, start: int, current: int, visited: list[int], distance_inc: int | float, distance_wanted: int | float) -> tuple[int, bool]:
	distance_left = distance_inc - t.distance(t.Coord.from_node(graph.nodes[current]), t.Coord.from_node(graph.nodes[visited[-1]]))
	# print(f"{current}: {distance_inc} -> {distance_left}")
	air_distance = t.distance(t.Coord.from_node(graph.nodes[start]), t.Coord.from_node(graph.nodes[current]))
	if distance_left < 0 and air_distance > distance_wanted * 0.8:
		return current, True
	elif air_distance > distance_wanted * 1.2:
		return -1, False

	visited.append(current)

	neighbours = list(iter(graph[current]))
	r.shuffle(neighbours)

	for node_id in neighbours:
		if node_id in visited:
			continue

		current_new, final = _quest_recursive(graph, start, node_id, visited, distance_left, distance_wanted)
		if final:
			return current_new, final

	return -1, False


def get_quest_point(graph: nx.MultiDiGraph, current_pos: t.Coord, distance_wanted: int) -> t.Coord:
	"""
	# TODO: write description
	@param graph:
	@param current_pos: starting position's coordinates
	@param distance_wanted: in meters
	@return:
	"""
	as_utm = current_pos.as_utm()
	node, dist = ox.nearest_nodes(graph, as_utm[0], as_utm[1], return_dist = True)
	node: int
	dist: float
	distance_left: float = distance_wanted - dist
	visited: list[int] = [node]

	quest_node_id, _ = _quest_recursive(graph, node, node, visited, distance_left, distance_wanted)
	return t.Coord.from_node(graph.nodes[quest_node_id], "red")


def multi_checker(distance_wanted):
	graph = get_graph()
	start = t.Coord(66.48208302041893, 25.722161963591045, "green")
	coordinates = [start]
	for _ in range(500):
		coordinates.append(get_quest_point(graph, start, distance_wanted))

	show_graph(graph, coordinates)


multi_checker(1200)
