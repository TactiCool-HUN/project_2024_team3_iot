import sqlite3


class DatabaseConnection:
	def __init__(self, host):
		self.connection = None
		if host[-3:] == ".db":
			self.host = f"save/{host}"
		else:
			self.host = f"save/{host}.db"

	def __enter__(self):
		self.connection = sqlite3.connect(self.host)
		return self.connection

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.connection.commit()
		self.connection.close()


def assure_database():
	with DatabaseConnection('activities') as con:
		cursor = con.cursor()
		cursor.execute(
			'CREATE TABLE IF NOT EXISTS quests('
			'id INTEGER,'
			'date INTEGER NOT NULL,'
			'time INTEGER NOT NULL,'
			'target_latitude REAL NOT NULL,'
			'target_longitude REAL NOT NULL,'
			'distance INTEGER NOT NULL,'  # in meters
			'accuracy INTEGER NOT NULL,'  # in meters
			'completed INTEGER NOT NULL,'  # 1 / 0 for yes / no
			'PRIMARY KEY(id)'
			')'
		)

		cursor.execute(
			'CREATE TABLE IF NOT EXISTS passive_movement('
			'id INTEGER,'
			'date INTEGER NOT NULL,'
			'distance INTEGER NOT NULL,'
			'PRIMARY KEY(id)'
			')'
		)


assure_database()
