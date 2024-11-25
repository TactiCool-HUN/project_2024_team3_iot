from math import sqrt, radians
from datetime import datetime
from functions.activity_saver import DatabaseConnection
from functions.settings import get_setting
import utm
UTM_REGION = 35
STEPS_TO_METERS = 0.75


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


def get_current_distance(goal_unit: str = 'meters') -> float:
	now = datetime.now()
	with DatabaseConnection('main') as con:
		cursor = con.cursor()
		cursor.execute(
			'SELECT distance '
			'FROM quests '
			'WHERE completed = 1 '
			'AND date = ?',
			(
				int(f'{now.year}{now.month}{now.day}')
			)
		)
		raw_quests = cursor.fetchall()

	quest_distance = sum([x[0] for x in raw_quests])

	with DatabaseConnection('main') as con:
		cursor = con.cursor()
		cursor.execute(
			'SELECT distance FROM passive_movement '
			'WHERE date = ?',
			(
				int(f'{now.year}{now.month}{now.day}')
			)
		)
		raw_passive = cursor.fetchall()

	passive_distance = sum([x[0] for x in raw_passive])
	full = quest_distance + passive_distance

	match goal_unit:
		case 'steps':
			return full * 1.4
		case 'meters':
			return full


def get_last_coordinates() -> Coord:
	with DatabaseConnection('main') as con:
		cursor = con.cursor()
		cursor.execute(
			'SELECT MAX(id) FROM passive_movement '
			'WHERE latitude IS NOT NULL AND longitude IS NOT NULL'
		)
		int_id = cursor.fetchall()[0]
		cursor.execute(
			'SELECT latitude, longitude FROM passive_movement '
			'WHERE id = ?',
			int_id
		)
		raw = cursor.fetchall()[0]

	return Coord(raw[0], raw[1])


pass
