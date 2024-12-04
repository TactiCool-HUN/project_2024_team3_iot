import os
import functions.settings as s
import functions.activity_saver as a_s
import utils.tools as t


def main():
	current = t.get_last_coordinates()
	quest_location = t.get_current_quest_coordinates()

	if quest_location is False:
		return

	accuracy = t.distance(current, quest_location)
	print(f'accuracy: {accuracy} meters away')
	if accuracy < 50:
		print('quest complete noted')
		with a_s.DatabaseConnection('main') as con:
			cursor = con.cursor()
			cursor.execute(
				'UPDATE quests '
				'SET accuracy = ? '
				'WHERE completed = 0',
				(accuracy,)
			)

	with a_s.DatabaseConnection('main') as con:
		cursor = con.cursor()
		cursor.execute(
			'SELECT * FROM quests WHERE completed = 0'
		)
		raw = cursor.fetchall()[0]

	if raw[5] is not None and accuracy > 100:
		print('quest_complete registered')
		with a_s.DatabaseConnection('main') as con:
			cursor = con.cursor()
			cursor.execute(
				'UPDATE quests '
				'SET completed = 1 '
				'WHERE completed = 0'
			)

		try:
			os.remove('./functions/save/current_quest.png')
		except FileNotFoundError:
			pass


if __name__ == '__main__':
	main()
