import utils.tools as t
import functions.settings as s
import random as r
import functions.location_quest as q


def main():
	goal = s.get_setting('daily_goal_steps') * t.STEPS_TO_METERS
	current = t.get_current_distance()
	remaining = goal - current
	if remaining < 0:
		return None

	start_time = s.get_setting('earliest_walk')
	end_time = s.get_setting('latest_walk')

	# converting to minutes
	start_time = int(str(start_time)[:-2]) * 60 + int(str(start_time)[-2:])
	end_time = int(str(end_time)[:-2]) * 60 + int(str(end_time)[-2:])

	current_time = t.datetime.now().hour * 60 + t.datetime.now().minute
	day_elapsed = (current_time - start_time) / (end_time - start_time)

	expected_point = goal * day_elapsed
	behind_by = expected_point - remaining
	current_pos: t.Coord = t.get_last_coordinates()
	if behind_by < -200:
		return None
	to_walk: int = round(behind_by * r.randint(10, 14) / 10)

	graph = q.get_graph()
	quest_point: t.Coord = q.get_quest_point(graph, current_pos, to_walk)


if __name__ == '__main__':
	main()
