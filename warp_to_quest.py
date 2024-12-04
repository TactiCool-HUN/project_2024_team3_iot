import functions.settings as s
import functions.activity_saver as a_s
import utils.tools as t


def warp_to(place: t.Coord) -> None:
	print(f'warping to {place}')
	with a_s.DatabaseConnection('main') as con:
		cursor = con.cursor()
		cursor.execute(
			'INSERT INTO passive_movement('
			'date,'
			'distance,'
			'latitude,'
			'longitude) '
			'VALUES (?, ?, ?, ?)',
			(
				20241204,
				0,
				place.latitude,
				place.longitude,
			)
		)


if __name__ == '__main__':
	qst = t.get_current_quest_coordinates()
	qst.longitude = qst.longitude - 0.000000000000275
	warp_to(qst)
	warp_to(t.Coord(66.4809296536252, 25.721840601334275))
