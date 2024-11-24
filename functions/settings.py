import os
from multiprocessing.managers import Value

from numpy.distutils.system_info import NotFoundError

FILEPATH = './save/settings.txt'
DEFAULT = \
	"""daily_goal_steps = 8750
earliest_walk = 0800
latest_walk = 2000"""


def _assure_settings_file():
	if os.path.isfile(FILEPATH):
		return

	with open(FILEPATH, 'w') as f:
		f.write(DEFAULT)

	_verify_settings_file()


def _verify_settings_file(crashing: bool = True) -> bool:
	"""
	Returns True if the settings file successfully validates, raises exception if it does not.
	Expected exceptions: FileNotFoundError; ValueError
	@param crashing: if set to false it will simply return a False instead of raising an exception
	@return:
	"""
	if not os.path.isfile(FILEPATH):
		if crashing:
			raise FileNotFoundError
		else:
			return False

	setting_names = [
		'daily_goal_steps',
		'earliest_walk',
		'latest_walk',
	]

	with open(FILEPATH, 'r') as f:
		lines = f.readlines()

	for line in lines:
		setting_name = line.split(' = ')[0]
		if setting_name in setting_names:
			setting_names.remove(setting_name)
		elif crashing:
			raise ValueError(f'Setting name > {setting_name} < not recognized.')
		else:
			return False

	if len(setting_names) != 0:
		if crashing:
			raise ValueError(f'Following setting name(s) not found: {", ".join(setting_names)}')
		else:
			return False

	return True


def get_setting(setting_name: str) -> str | float:
	with open(FILEPATH, 'r') as f:
		lines = f.readlines()

	for line in lines:
		line = line.split(' = ')
		if line[0] == setting_name:
			try:
				return float(line[1])
			except ValueError:
				return line[1]

	_verify_settings_file()
	raise ValueError(f'Setting name > {setting_name} < is not recognized.')


_assure_settings_file()
