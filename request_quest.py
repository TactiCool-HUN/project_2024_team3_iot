import utils.tools as t
import functions.settings as s
import functions.activity_saver as a_s
import random as r
import functions.location_quest as q
from functions.activity_saver import DatabaseConnection
from datetime import datetime


def main():
	goal = s.get_setting('daily_goal_steps') * t.STEPS_TO_METERS
	current = t.get_current_distance()
	remaining = goal - current
	if remaining < 0:
		return None

	start_time = int(s.get_setting('earliest_walk'))
	end_time = int(s.get_setting('latest_walk'))

	# converting to minutes
	start_time = int(str(start_time)[:-2]) * 60 + int(str(start_time)[-2:])
	end_time = int(str(end_time)[:-2]) * 60 + int(str(end_time)[-2:])

	current_time = 600  # t.datetime.now().hour * 60 + t.datetime.now().minute
	day_elapsed = (current_time - start_time) / (end_time - start_time)

	expected_point = goal * day_elapsed
	behind_by = expected_point - current
	current_pos: t.Coord = t.get_last_coordinates()
	if behind_by < -200:
		return None
	to_walk: int = round(behind_by * r.randint(10, 14) / 10)

	graph = q.get_graph()
	quest_point: t.Coord = q.get_quest_point(graph, current_pos, to_walk)

	now = datetime.now()
	month = now.month
	if month < 10:
		month = f'0{month}'
	day = now.day
	if day < 10:
		day = f'0{day}'
	date = int(f'{now.year}{month}{day}')
	hour = now.hour
	minute = now.minute
	if minute < 10:
		minute = f'0{minute}'
	time = int(f'{hour}{minute}')

	with DatabaseConnection('main') as con:
		cursor = con.cursor()
		cursor.execute(
			'INSERT INTO quests('
			'date,'
			'time,'
			'target_latitude,'
			'target_longitude,'
			'accuracy,'
			'completed) '
			'VALUES (?, ?, ?, ?, ?, ?)',
			(
				date,
				time,
				quest_point.latitude,
				quest_point.longitude,
				None,
				0
			)
		)

	q.save_graph(graph, 'current_quest', [current_pos, quest_point], show_after_save = True)


if __name__ == '__main__':
	a_s.destroy_database()
	a_s.assure_database()
	a_s.make_totally_real_data_tm()
	main()
