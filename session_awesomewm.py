__kupfer_name__ = _("awesome Session Management")
__kupfer_sources__ = ("AwesomeItemsSource", )
__description__ = _("Special items and actions for awesome environment")
__version__ = "2011-03-27"
__author__ = "Jakh Daven <tuxcanfly@gmail.com>"

import dbus

from kupfer.plugin import session_support as support
from kupfer.obj.objects import RunnableLeaf

# sequences of argument lists
LOGOUT_CMD = (["gnome-panel-logout"],
              ["gnome-session-save", "--kill"])
LOCKSCREEN_CMD = (["gnome-screensaver-command", "--lock"],
                  ["xdg-screensaver", "lock"])
CONSOLEKIT_IFACE = 'org.freedesktop.ConsoleKit'
CONSOLEKIT_PATH = '/org/freedesktop/ConsoleKit/Manager'
COMMAND_IFACE = 'org.freedesktop.ConsoleKit.Manager'

def _create_dbus_connection():
	interface = None
	sbus = dbus.SystemBus()
	proxy_obj = sbus.get_object(CONSOLEKIT_IFACE, CONSOLEKIT_PATH)
	return proxy_obj


class SessionCommand (RunnableLeaf):
	"""Base Session Command"""

	def __init__(self, obj=None, name=None):
		RunnableLeaf.__init__(self, obj=obj, name=name)

	def run(self, ctx=None):
		consolekit_iface = _create_dbus_connection()
		getattr(consolekit_iface, self.name)()

	def get_description(self):
		return _("%ss the computer" %self.name)

class AwesomeItemsSource (support.CommonSource):
	def __init__(self):
		support.CommonSource.__init__(self, _("awesome Session Management"))
	def get_items(self):
		return (
			support.Logout(LOGOUT_CMD),
			support.LockScreen(LOCKSCREEN_CMD),
			SessionCommand(name='Stop'),
			SessionCommand(name='Restart'),
			SessionCommand(name='Suspend'),
			SessionCommand(name='Hibernate'),
		)

