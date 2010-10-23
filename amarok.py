# vim: set noexpandtab ts=8 sw=8:
from __future__ import absolute_import

__kupfer_name__ = _("Amarok")
__kupfer_actions__ = ("StopAfterCurrent", "ShowOSD", "Play", 
                      "Pause", "Next", "Previous", "Mute")
__description__ = _("Control Amarok media player.")
__version__ = "2010-10-22"
__author__ = "Andreas Kotowicz <andreas.kotowicz@gmail.com>"

''' 
    TODO (don't know how to do these things):

        - start amarok if not running and user hits "play" (via dbus)

'''

import dbus

from kupfer.objects import Action, AppLeaf
from kupfer import icons, pretty


from kupfer import plugin_support
plugin_support.check_dbus_connection()

SERVICE_NAME = "org.kde.amarok"
OBJECT_PATH = "/Player"

def _get_amarok():
	""" Return the dbus proxy object for Amarok
	    we will activate it over d-bus (start if not running)
	"""
	bus = dbus.SessionBus()
	try:
		amarok_obj = bus.get_object(SERVICE_NAME, OBJECT_PATH)
	except dbus.DBusException, e:
		pretty.print_error(__name__, e)
		return
	return amarok_obj

class StopAfterCurrent (Action):
	def __init__(self):
		Action.__init__(self, name=_("StopAfterCurrent"))
	def activate(self, leaf, obj):
		_get_amarok().StopAfterCurrent()
	def item_types(self):
		yield AppLeaf
	def valid_for_item(self, leaf):
		return leaf.get_id() == "kde4-amarok"
	def get_description(self):
		return _("Stop Amarok playback after current song")
	def get_icon_name(self):
		return "media-playback-stop"

class ShowOSD (Action):
	def __init__(self):
		Action.__init__(self, name=_("Show OSD"))
	def activate(self, leaf, obj):
		_get_amarok().ShowOSD()
	def item_types(self):
		yield AppLeaf
	def valid_for_item(self, leaf):
		return leaf.get_id() == "kde4-amarok"
	def get_description(self):
		return _("Show  Amarok OSD")
	def get_gicon(self):
		return icons.ComposedIcon("dialog-information", "audio-x-generic")
	def get_icon_name(self):
		return "dialog-information"

class Play (Action):
	def __init__(self):
		Action.__init__(self, name=_("Play"))
	def activate(self, leaf, obj):
		_get_amarok().Play()
	def item_types(self):
		yield AppLeaf
	def valid_for_item(self, leaf):
		return leaf.get_id() == "kde4-amarok"
	def get_description(self):
		return _("Resume playback in Amarok")
	def get_icon_name(self):
		return "media-playback-start"

class Pause (Action):
	def __init__(self):
		Action.__init__(self, name=_("Pause"))
	def activate(self, leaf, obj):
		_get_amarok().Pause()
	def item_types(self):
		yield AppLeaf
	def valid_for_item(self, leaf):
		return leaf.get_id() == "kde4-amarok"
	def get_description(self):
		return _("Pause playback in Amarok")
	def get_icon_name(self):
		return "media-playback-pause"

class Next (Action):
	def __init__(self):
		Action.__init__(self, name=_("Next"))
	def activate(self, leaf, obj):
		_get_amarok().Next()
	def item_types(self):
		yield AppLeaf
	def valid_for_item(self, leaf):
		return leaf.get_id() == "kde4-amarok"
	def get_description(self):
		return _("Jump to next track in Amarok")
	def get_icon_name(self):
		return "media-skip-forward"

class Previous (Action):
	def __init__(self):
		Action.__init__(self, name=_("Previous"))
	def activate(self, leaf, obj):
		_get_amarok().Prev()
	def item_types(self):
		yield AppLeaf
	def valid_for_item(self, leaf):
		return leaf.get_id() == "kde4-amarok"
	def get_description(self):
		return _("Jump to previous track in Amarok")
	def get_icon_name(self):
		return "media-skip-backward"

class Mute (Action):
	def __init__(self):
		Action.__init__(self, name=_("Mute"))
	def activate(self, leaf, obj):
		_get_amarok().Mute()
	def item_types(self):
		yield AppLeaf
	def valid_for_item(self, leaf):
		return leaf.get_id() == "kde4-amarok"
	def get_description(self):
		return _("Mute / Unmute Amarok")
	def get_icon_name(self):
		return "audio-volume-muted"

# EOF
