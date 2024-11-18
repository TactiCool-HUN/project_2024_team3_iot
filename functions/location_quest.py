from utils import tools as t
import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
FILEPATH = "./save/"


def request_graph(
	address: str = "Hallituskatu 1A, 96100 Rovaniemi",
	distance: int = 5000,
	save: bool = True,
	save_name: str = "rovaniemi"
) -> nx.MultiDiGraph:
	"""
	Requests a graph from the API handler, also automatically saves it.
	@param address: custom center position
	@param distance: distance from center position, recommended 4000 - 10_000
	@param save: should the graph be saved?
	@param save_name: what name should the graph be saved at? (automatically overwrites existing files)
	@return:
	"""
	multi_graph = ox.graph_from_address(address, dist=distance, network_type="walk")
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
	graph = ox.consolidate_intersections(graph_proj, rebuild_graph=True, tolerance=15, dead_ends=False)
	return graph


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
	@param coords:
	@return:
	"""
	fig, ax = ox.plot_graph(graph, show = False, close = False)
	if coords:
		for coord in coords:
			coord.map_to_graph(ax)
	plt.show()


coordinates = t.Coord(66.49657, 25.7277)
show_graph(get_graph(), [coordinates])
