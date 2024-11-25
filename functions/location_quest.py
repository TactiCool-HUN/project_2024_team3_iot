from utils import tools as t
import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
import random as r

FILEPATH = "./save/"


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
	Get a random point on the graph that is within the set distance of start.
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


def request_quest():
	goal = t.get_setting('daily_goal_steps') * t.STEPS_TO_METERS
	current = t.get_current_distance()
	remaining = goal - current
	if remaining < 0:
		return None

	start_time = t.get_setting('earliest_walk')
	end_time = t.get_setting('latest_walk')
	# converting to minutes
	start_time = int(str(start_time)[:-2]) * 60 + int(str(start_time)[-2:])
	end_time = int(str(end_time)[:-2]) * 60 + int(str(end_time)[-2:])
	current_time = t.datetime.now().hour * 60 + t.datetime.now().minute
	day_elapsed = (current_time - start_time) / (end_time - start_time)

	expected_point = goal * day_elapsed
	behind_by = expected_point - remaining
	current_pos: t.Coord = t.get_last_coordinates()
	if behind_by > 0:
		to_walk: int = round(behind_by * r.randint(10, 12) / 10)
	else:
		to_walk: int = 200

	graph = get_graph()
	quest_point: t.Coord = get_quest_point(graph, current_pos, to_walk)




def tester():
	graph = get_graph()
	coordinates = []
	for _ in range(500):
		start = t.Coord(47 + r.randint(0, 10000) / 10000, 17 + r.randint(0, 10000) / 10000, "green")
		coordinates = [start]
		distance_wanted = r.randint(50, 4000)
		coordinates.append(get_quest_point(graph, start, distance_wanted))

	# show_graph(graph, coordinates)


# tester()
