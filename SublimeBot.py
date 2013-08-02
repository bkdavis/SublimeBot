import sublime
import sublime_plugin
from subprocess import call
import os

class SublimeBotViewFileName:
	base = None
	extension = None
	full = None

	def __init__(self, full):
		self.full = full
		self.base, self.extension = os.path.splitext(full)
		self.extension = self.extension.lstrip('.')


class SublimeBotViewFile:
	path = None
	directory = None
	name = None

	def __init__(self, path):
		self.path = path
		self.directory, nameFull = os.path.split(path)
		self.name = SublimeBotViewFileName(nameFull)


class SublimeBotViewProject:
	directory = None

	def __init__(self, directory):
		self.directory = directory


class SublimeBotView:
	file = None
	project = None
	view = None

	def __init__(self, view):
		self.view = view
		self.file = SublimeBotViewFile(view.file_name())
		self.project = SublimeBotViewProject(view.window().folders()[0])


class SublimeBotFileWatch:
	definition = None
	view = None

	def __init__(self, definition, view):
		self.definition = definition
		self.view = view

	@property
	def triggered(self):
		triggered = False

		definitionKeys = self.definition.keys()

		if 'file_directory' in definitionKeys and self.definition.get('file_directory') == self.view.file.directory:
			triggered = True

		if not triggered and 'file_path' in definitionKeys and self.definition.get('file_path') == self.view.file.path:
			triggered = True

		if not triggered and 'file_name_base' in definitionKeys and self.definition.get('file_name_base') == self.view.file.name.base:
			triggered = True

		if not triggered and 'file_name_full' in definitionKeys and self.definition.get('file_name_full') == self.view.file.name.full:
			triggered = True

		if not triggered and 'file_name_extension' in definitionKeys and self.definition.get('file_name_extension') == self.view.file.name.extension:
			triggered = True

		return triggered


class SublimeBotAction:
	definition = None
	view = None

	def __init__(self, definition, view):
		self.definition = definition
		self.view = view

	def run(self):
		if 'shell' in self.definition.keys():
			shell = self.definition.get('shell')

			shell.replace('%FILE_DIRECTORY%', self.view.file.directory)
			shell.replace('%FILE_PATH%', self.view.file.path)
			shell.replace('%FILE_NAME%', self.view.file.name.full)
			shell.replace('%FILE_NAME_BASE%', self.view.file.name.base)
			shell.replace('%FILE_NAME_FULL%', self.view.file.name.full)
			shell.replace('%FILE_NAME_EXTENSION%', self.view.file.name.extension)
			shell.replace('%PROJECT_DIRECTORY%', self.view.project.directory)

			shellParts = shell.split(' ')
			print('shellParts', shellParts)
			call(shellParts)


class SublimeBot:
	events = None
	settings = None

	def __init__(self, settings):
		self.settings = settings
		self.events = settings.get('SublimeBot')

	def postSaveAsync(self, view):
		view = SublimeBotView(view)

		for eventName, event in self.events.items():
			if eventName.find('#') != 0:
				if set(['watch', 'action']).issubset(set(event.keys())):
					watch = SublimeBotFileWatch(event.get('watch'), view)

					if watch.triggered:
						action = SublimeBotAction(event.get('action'), view)
						action.run()


class SublimeBotEvent(sublime_plugin.EventListener):
	bot = None

	def on_post_save_async(self, view):
		settings = sublime.load_settings('SublimeBot.sublime-settings')
		self.bot = SublimeBot(settings)
		self.bot.postSaveAsync(view)
