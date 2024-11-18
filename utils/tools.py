from math import sin, cos, sqrt, atan2, radians
import utm


class Coord:
	def __init__(self, latitude: float, longitude: float, in_rad: bool = True):
		if in_rad:
			self.latitude = latitude
			self.longitude = longitude
		else:
			self.latitude = radians(latitude)
			self.longitude = radians(longitude)

	def __add__(self, other):
		if isinstance(other, Coord):
			return Coord(
				self.latitude + other.latitude,
				self.longitude + other.longitude,
				in_rad = True
			)

		raise TypeError(f"Coord class cannot be added to {type(other)}")

	def __sub__(self, other):
		if isinstance(other, Coord):
			return Coord(
				self.latitude - other.latitude,
				self.longitude - other.longitude,
				in_rad = True
			)

		raise TypeError(f"Coord class cannot be subtracted from {type(other)}")

	def __bool__(self):
		return self.longitude != 0 and self.latitude != 0

	def __eq__(self, other):
		if isinstance(other, Coord):
			return self.latitude == other.latitude and self.longitude == other.longitude

		raise TypeError(f"Coord class cannot be subtracted from {type(other)}")

	def __str__(self):
		return f"({self.latitude}, {self.longitude})"

	def map_to_graph(self, ax, c: str = "red") -> None:
		"""
		Places coordinates onto a graph.
		@param ax: Axis gotten from an active matplotlib plot.
		@param c: Color of the coordinate point.
		@return:
		"""
		x, y, _, _ = utm.from_latlon(self.latitude, self.longitude)
		ax.scatter(x, y, c = c)


def distance(point_1, point_2) -> float:
	d_coords = point_2 - point_1

	a = sin(d_coords.latitude / 2) ** 2 + cos(point_1.latitude) * cos(point_2.latitude) * sin(d_coords.longitude / 2) ** 2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	return 6373.0 * c  # c * approx. radius of Earth
