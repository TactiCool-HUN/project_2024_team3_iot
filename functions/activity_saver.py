import os
import sqlite3
from functions.settings import get_setting, set_setting


class DatabaseConnection:
	def __init__(self, host):
		self.connection = None
		if host[-3:] == ".db":
			self.host = f"functions/save/{host}"
		else:
			self.host = f"functions/save/{host}.db"

	def __enter__(self):
		self.connection = sqlite3.connect(self.host)
		return self.connection

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.connection.commit()
		self.connection.close()


def destroy_database():
	try:
		os.remove('functions/save/main.db')
	except FileNotFoundError:
		return


def soft_purge():
	with DatabaseConnection('main') as con:
		cursor = con.cursor()
		cursor.execute(
			'DROP TABLE IF EXISTS raw_sensor_data'
		)


def assure_database():
	with DatabaseConnection('main') as con:
		cursor = con.cursor()
		cursor.execute(
			'CREATE TABLE IF NOT EXISTS quests('
			'id INTEGER,'
			'date INTEGER NOT NULL,'
			'time INTEGER NOT NULL,'
			'target_latitude REAL NOT NULL,'
			'target_longitude REAL NOT NULL,'
			'distance INTEGER NOT NULL,'  # in meters
			'accuracy INTEGER,'  # in meters
			'completed INTEGER NOT NULL,'  # 1 / 0 for yes / no
			'PRIMARY KEY(id)'
			')'
		)

		cursor.execute(
			'CREATE TABLE IF NOT EXISTS passive_movement('
			'id INTEGER,'
			'date INTEGER NOT NULL,'
			'distance INTEGER NOT NULL,'
			'latitude REAL,'
			'longitude REAL,'
			'PRIMARY KEY(id)'
			')'
		)

		cursor.execute(
			'CREATE TABLE IF NOT EXISTS raw_sensor_data('
			'id INTEGER,'
			'date INTEGER NOT NULL,'
			'latitude REAL,'
			'longitude REAL,'
			'acc_x REAL,'
			'acc_y REAL,'
			'acc_z REAL,'
			'processed INTEGER DEFAULT 0,'
			'PRIMARY KEY(id)'
			')'
		)


def make_totally_real_data_tm():
	with DatabaseConnection('main') as con:
		cursor = con.cursor()
		cursor.execute(
			'INSERT INTO passive_movement('
			'date,'
			'distance,'
			'latitude,'
			'longitude) '
			'VALUES (?, ?, ?, ?)',
			(
				20241124,
				100,
				20,
				25
			)
		)
		cursor.execute(
			'INSERT INTO passive_movement('
			'date,'
			'distance,'
			'latitude,'
			'longitude) '
			'VALUES (?, ?, ?, ?)',
			(
				20241124,
				150,
				30,
				35
			)
		)
		cursor.execute(
			'INSERT INTO passive_movement('
			'date,'
			'distance,'
			'latitude,'
			'longitude) '
			'VALUES (?, ?, ?, ?)',
			(
				20241124,
				125,
				None,
				None
			)
		)


print('check: hard_purge')
if int(get_setting('hard_purge_database')) == 1:
	destroy_database()
	set_setting('hard_purge_database', 0)

print('check: soft_purge')
if int(get_setting('soft_purge_database')) == 1:
	soft_purge()
	set_setting('soft_purge_database', 0)

print('assure database')
assure_database()
# make_totally_real_data_tm()
