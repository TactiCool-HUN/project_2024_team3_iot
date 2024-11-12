from math import sin, cos, sqrt, atan2, radians

# Approximate radius of earth in km
R = 6373.0


class Coord:
	def __init__(self, latitude: float, longitude: float, in_rad: bool = False):
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


point_1 = Coord(52.2296756, 21.0122287)
point_2 = Coord(52.4063740, 16.9251681)

d_coords = point_2 - point_1

a = sin(d_coords.latitude / 2) ** 2 + cos(point_1.latitude) * cos(point_2.latitude) * sin(d_coords.longitude / 2) ** 2
c = 2 * atan2(sqrt(a), sqrt(1 - a))

distance = R * c

print("Result: ", distance)
print("Should be: ", 278.546, "km")