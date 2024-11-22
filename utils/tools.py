from math import sin, cos, sqrt, atan2, radians
import utm
UTM_REGION = 35


class Coord:
	def __init__(self, latitude: float, longitude: float, colour: str = None, convert_from: str = "none"):
		"""
		@param latitude:
		@param longitude:
		@param convert_from: options: degrees, utm
		"""
		match convert_from:
			case "degrees":
				self.latitude = radians(latitude)
				self.longitude = radians(longitude)
			case "utm":
				self.latitude, self.longitude = utm.to_latlon(latitude, longitude, UTM_REGION, northern = True)
			case _:
				self.latitude = latitude
				self.longitude = longitude

		self.colour = colour

	def __add__(self, other):
		if isinstance(other, Coord):
			return Coord(
				self.latitude + other.latitude,
				self.longitude + other.longitude
			)

		raise TypeError(f"Coord class cannot be added to {type(other)}")

	def __sub__(self, other):
		if isinstance(other, Coord):
			return Coord(
				self.latitude - other.latitude,
				self.longitude - other.longitude
			)

		raise TypeError(f"Coord class cannot be subtracted from {type(other)}")

	def __bool__(self):
		return self.latitude != 0 and self.longitude != 0

	def __eq__(self, other):
		if isinstance(other, Coord):
			return self.latitude == other.latitude and self.longitude == other.longitude

		raise TypeError(f"Coord class cannot be subtracted from {type(other)}")

	def __str__(self):
		return f"({self.latitude}, {self.longitude})"

	@staticmethod
	def from_node(node, colour: str = None):
		return Coord(node['x'], node['y'], colour, "utm")

	def as_utm(self):
		return utm.from_latlon(self.latitude, self.longitude)

	def map_to_graph(self, ax) -> None:
		"""
		Places coordinates onto a graph.
		@param ax: Axis gotten from an active matplotlib plot.
		@return:
		"""
		x, y, _, _ = utm.from_latlon(self.latitude, self.longitude)
		ax.scatter(x, y, c = self.colour)


def distance(point_1: Coord, point_2: Coord) -> float:
	x1, y1, _, _ = point_1.as_utm()
	x2, y2, _, _ = point_2.as_utm()

	dx = x2 - x1
	dy = y2 - y1

	return sqrt(dx ** 2 + dy ** 2)
