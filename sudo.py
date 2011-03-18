# vim: set noexpandtab ts=8 sw=8:

__kupfer_name__ = _("Sudo")
__kupfer_actions__ = (
		"OpenAsRoot",
	)
__description__ = _("Open selection application with root priveleges")
__version__ = ""
__author__ = "Jakh Daven <tuxcanfly@gmail.com>"

from kupfer.objects import Action, AppLeaf
from kupfer import plugin_support
from kupfer.utils import launch_commandline
from kupfer import pretty

__kupfer_settings__ = plugin_support.PluginSettings(
	{
		"key" : "sudo_command",
		"label": _("Sudo Command"),
		"type": str,
		"value": "gksu",
		"alternatives": ("kdesudo", )
	},
)

class OpenAsRoot (Action):
	def __init__(self):
		Action.__init__(self, _("Open as root"))

	def activate(self, leaf):
		cmd = "%s %s" %(__kupfer_settings__["sudo_command"],
				leaf.object.get_commandline())
		ret = launch_commandline(cmd)
		if ret: return ret
		pretty.print_error(__name__, "Unable to run command(s)", cmd)

	def activate_multiple(self, objects, iobjects):
		for iobj_app in iobjects:
			self.activate(iobj_app.object, [L.object for L in objects])

	def item_types(self):
		yield AppLeaf
	def get_description(self):
		return _("Open with root priveleges")

