import functions.activity_saver as a_s
import utils.tools as t


def main():
	with a_s.DatabaseConnection('main') as con:
		cursor = con.cursor()
		cursor.execute(
			'SELECT id, date, latitude, longitude, acc_x, acc_y, acc_z FROM raw_sensor_data WHERE processed = 0'
		)
		raw = cursor.fetchall()

	for data in raw:
		current_id = data[0]
		date = data[1]
		latitude = data[2]
		longitude = data[3]
		acc_x = data[4]
		acc_y = data[5]
		acc_z = data[6]

		if latitude and longitude:
			last_coords = t.get_last_coordinates()
			current_coords = t.Coord(latitude, longitude)
			distance = t.distance(last_coords, current_coords)

			with a_s.DatabaseConnection('main') as con:
				cursor = con.cursor()
				cursor.execute(
					'INSERT INTO passive_movements('
					'date,'
					'distance,'
					'latitude,'
					'longitude) '
					'VALUES (?, ?, ?, ?)',
					(
						date,
						distance,
						latitude,
						longitude
					)
				)
		else:
			distance = 10  # TODO: magic
			with a_s.DatabaseConnection('main') as con:
				cursor = con.cursor()
				cursor.execute(
					'INSERT INTO passive_movements('
					'date,'
					'distance) '
					'VALUES (?, ?)',
					(
						date,
						distance
					)
				)

		with a_s.DatabaseConnection('main') as con:
			cursor = con.cursor()
			cursor.execute(
				'UPDATE raw_sensor_data '
				'SET processed = 1 '
				'WHERE id = ?',
				(current_id,)
			)


if __name__ == '__main__':
	main()
