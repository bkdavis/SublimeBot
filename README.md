SublimeBot
====================

Sublime Text plugin for executing custom automated tasks when view events are triggered.

Right now, I've just implemented triggers related to saving files (inspired by the CommandOnSave plugin) but intend to extend it to all view event listeners (http://www.sublimetext.com/docs/2/api_reference.html#sublime_plugin.EventListener).

The default settings file contains samples of all current watch options for file saving.  The basic idea is that you define a watch for a particular event and an action to be run when that event/watch finds a match.  Currently, you can only run a shell command (passed on to Python's subprocess call) but I intend to extend this to run python scripts, etc.

If you use this, please let me know what the most useful scenarios are for you and I'll work on those first.
