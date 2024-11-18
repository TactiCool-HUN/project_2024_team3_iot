from utils import tools as t
import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
filepath = "./save/rovaniemi.graphml"

"""
G = ox.graph_from_address("Hallituskatu 1A, 96100 Rovaniemi", dist=5000, network_type="walk")
ox.save_graphml(G, filepath)
"""


G = ox.load_graphml(filepath)

G_proj = ox.project_graph(G)
G = ox.consolidate_intersections(G_proj, rebuild_graph=True, tolerance=15, dead_ends=False)

fig, ax = ox.plot_graph(G, show = False, close = False)
ax.scatter(443400, 7375900, c="red")
plt.show()
