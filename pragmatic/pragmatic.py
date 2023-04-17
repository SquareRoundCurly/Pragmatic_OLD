from typing import Callable, Dict, Any, List, Tuple
import string

from typeguard import typechecked

commands: dict[str, List[Tuple[List[str], str]]] = {}
rules: List[Tuple[str, str, str]] = []

@typechecked
def format_command(command: str, config: Dict[str, Any], include_partial: bool = False) -> List[Tuple[List[str], str]]:
	class CommandFormatter(string.Formatter):
		def __init__(self, delayed: List[str]):
			self.partial = False
			self.delayed = delayed
		
		def get_value(self, key, args, kwargs):
			if key in self.delayed:
				return f'{{{key}}}'

			if self.partial:
				return kwargs.get(key, "")
			else:
				return super().get_value(key, args, kwargs)
			
		def format(self, *args, **kwargs):
			self.partial = kwargs.pop('partial', self.partial)
			result = super().format(*args, **kwargs)
			self.partial = False  # Reset the partial flag to its default value
			return result

	formatted_commands: List[Tuple[List[str], str]] = []
	command_formatter = CommandFormatter(['input', 'output'])

	@typechecked
	def add_formatted_command(key_path: List[str], formatted_command: str) -> None:
		nonlocal formatted_commands
		if not key_path: return
		formatted_commands.append((key_path, formatted_command))

	@typechecked
	def traverse_config(dictionary: Dict[str, Any], current_config: Dict[str, str], key_path: List[str] = []) -> None:
		for key, value in dictionary.items():
			new_key_path = key_path + [key]
			if isinstance(value, dict):
				traverse_config(value, current_config.copy(), new_key_path)
			elif isinstance(value, str):
				current_config[key] = value

		try:
			formatted_command = command_formatter.format(command, **current_config, partial=include_partial)
			add_formatted_command(key_path, formatted_command)
		except KeyError:
			pass # The case when the current_config does not contain the required key for formatting

	if not config:
		raise ValueError('Config must not be empty')

	traverse_config(config, {})

	return formatted_commands

@typechecked
def add_command(command_name: str, command: str, config: dict[str, Any]) -> None:
	global commands
	
	command_list = format_command(command, config, include_partial=True)
	commands[command_name] = command_list

@typechecked
def add_rule(input: str, output: str, command_name: str) -> None:
	global rules

	rules.append((input, output, command_name))