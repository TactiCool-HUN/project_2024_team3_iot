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
	if accuracy < 50:
		with a_s.DatabaseConnection('main') as con:
			cursor = con.cursor()
			cursor.execute(
				'UPDATE quests(accuracy = ?) WHERE completed = 0',
				(accuracy,)
			)

	with a_s.DatabaseConnection('main') as con:
		cursor = con.cursor()
		cursor.execute(
			'SELECT * FROM quests WHERE completed = 0'
		)
		raw = cursor.fetchall()[0]

	if raw[6] is not None:
		if raw[6] > accuracy + 100:
			with a_s.DatabaseConnection('main') as con:
				cursor = con.cursor()
				cursor.execute(
					'UPDATE quests(completed = 1) WHERE completed = 0'
				)

			try:
				os.remove('./functions/save/current_quest.png')
			except FileNotFoundError:
				pass


if __name__ == '__main__':
	main()
