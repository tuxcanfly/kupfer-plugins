# vim: set noexpandtab ts=8 sw=8:

__kupfer_name__ = _("Sudo")
__kupfer_actions__ = (
		"OpenAsRoot",
	)
__description__ = _("Open selection with root priveleges")
__version__ = ""
__author__ = "Jakh Daven <tuxcanfly@gmail.com>"

from kupfer.objects import Action, Leaf, FileLeaf, AppLeaf
from kupfer import plugin_support
from kupfer.utils import launch_commandline
from kupfer import pretty
from kupfer.obj.fileactions import Open

__kupfer_settings__ = plugin_support.PluginSettings(
	{
		"key" : "sudo_command",
		"label": _("Sudo Command"),
		"type": str,
		"value": "gksudo",
		"alternatives": ("kdesudo", )
	},
)

class OpenAsRoot (Open):
	def __init__(self):
		Action.__init__(self, _("Open as root"))

	def activate(self, leaf):
		if type(leaf) == AppLeaf:
		    cmd = "%s %s" %(__kupfer_settings__["sudo_command"],
				leaf.object.get_commandline())
		    ret = launch_commandline(cmd)
		    if ret: return ret
		    pretty.print_error(__name__, "Unable to run command(s)", cmd)
		elif type(leaf) == FileLeaf:
			self.activate_multiple((leaf, ))

	def activate_multiple(self, objects):
		appmap = {}
		leafmap = {}
		for iobj_app in objects:
			if type(iobj_app) == AppLeaf:
			    self.activate(iobj_app.object, [L.object for L in objects])
			elif type(iobj_app) == FileLeaf:
				app = self.default_application_for_leaf(iobj_app)
				id_ = app.get_id()
				appmap[id_] = app
				leafmap.setdefault(id_, []).append(iobj_app)

		for id_, leaves in leafmap.iteritems():
			app = appmap[id_]
			cmd = "%s %s " %(__kupfer_settings__["sudo_command"],
					app.get_commandline())
			for l in leaves:
				cmd += "%s " %l.object
			ret = launch_commandline(cmd)
			if ret: return ret
			pretty.print_error(__name__, "Unable to run command(s)", cmd)

	def item_types(self):
		yield Leaf
	def get_description(self):
		return _("Open with root priveleges")

