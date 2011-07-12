__kupfer_name__ = _("VolumeControl")
__kupfer_sources__ = ("VolumeControlSource", )
__description__ = _("Simple Plugin to Control the system volume. It includes Mute, Unmute, Volume Up, Volume Down and VolumeMax.")
__version__ = "2010-11-18"
__author__ = "Rafael Brundo Uriarte<rafael.uriarte@gmail.com>"

import subprocess
from kupfer.objects import Source
from kupfer.objects import RunnableLeaf
from kupfer.obj.apps import AppLeafContentMixin
from kupfer import utils, uiutils

class VolumeNotifier():
	def __init__(self):
		VolumeNotifier.nid = 0
	def show_notification(self, title, body, icon_name):
		VolumeNotifier.nid = uiutils.show_notification(title, body, icon_name, VolumeNotifier.nid)

class Mute (RunnableLeaf, VolumeNotifier):
	def __init__(self):
		RunnableLeaf.__init__(self, name=_("Mute"))
		VolumeNotifier.__init__(self)
	def run(self):
		#check if is not muted already
		#proc = subprocess.Popen('/usr/bin/amixer sget Master', shell=True, stdout=subprocess.PIPE)
		#result = str(proc.communicate())
		#if "off" not in result:
		utils.launch_commandline("amixer sset Master,0 mute", in_terminal=False)
		title, body = "Volume", "Muted"
		self.show_notification(title, body, icon_name=self.get_icon_name())

	def get_description(self):
		return _("Mute Volume")
	def get_icon_name(self):
		return "stock_volume-mute"

class UnMute (RunnableLeaf, VolumeNotifier):
	def __init__(self):
		RunnableLeaf.__init__(self, name=_("UnMute"))
		VolumeNotifier.__init__(self)
	def run(self):
		utils.launch_commandline("amixer sset Master unmute", in_terminal=False)
		title, body = "Volume", "UnMuted"
		self.show_notification(title, body, icon_name=self.get_icon_name())
	def get_description(self):
		return _("UnMute the Volume")
	def get_icon_name(self):
		return "stock_volume"

class VolumeUp (RunnableLeaf, VolumeNotifier):
	def __init__(self):
		RunnableLeaf.__init__(self, name=_("VolumeUp"))
		VolumeNotifier.__init__(self)
	def run(self):
		utils.launch_commandline("amixer sset Master,0 6+", in_terminal=False)
		title= "Volume"
		body = "Up, now is %s"%int(self.get_master_volume())
		self.show_notification(title, body+"%", icon_name=self.get_icon_name())
	def get_description(self):
		return _("Volume Up")
	def get_icon_name(self):
		return "stock_volume-med"
	def get_master_volume(self):
       		proc = subprocess.Popen('/usr/bin/amixer sget Master', shell=True, stdout=subprocess.PIPE)
		amixer_stdout = proc.communicate()[0].split('\n')[4]
		proc.wait()

		find_start = amixer_stdout.find('[') + 1
		find_end = amixer_stdout.find('%]', find_start)
		return float(amixer_stdout[find_start:find_end])

class VolumeDown (RunnableLeaf, VolumeNotifier):
	def __init__(self):
		RunnableLeaf.__init__(self, name=_("VolumeDown"))
		VolumeNotifier.__init__(self)
	def run(self):
		utils.launch_commandline("amixer sset Master,0 6-", in_terminal=False)
		title = "Volume"
		body = "Down, now is %s"%int(self.get_master_volume())
		self.show_notification(title, body+"%", icon_name=self.get_icon_name())
	def get_description(self):
		return _("Volume Down")
	def get_icon_name(self):
		return "stock_volume-min"
	def get_master_volume(self):
       		proc = subprocess.Popen('/usr/bin/amixer sget Master', shell=True, stdout=subprocess.PIPE)
		amixer_stdout = proc.communicate()[0].split('\n')[4]
		proc.wait()

		find_start = amixer_stdout.find('[') + 1
		find_end = amixer_stdout.find('%]', find_start)
		return float(amixer_stdout[find_start:find_end])

class VolumeMax (RunnableLeaf, VolumeNotifier):
	def __init__(self):
		RunnableLeaf.__init__(self, name=_("VolumeMax"))
		VolumeNotifier.__init__(self)
	def run(self):
		utils.launch_commandline("amixer sset Master 100", in_terminal=False)
		title, body = "Volume", "100%"
		self.show_notification(title, body, icon_name=self.get_icon_name())
	def get_description(self):
		return _("Volume 100%")
	def get_icon_name(self):
		return "stock_volume-max"




class VolumeControlSource (AppLeafContentMixin, Source):
	appleaf_content_id = "Volume Control"
	source_user_reloadable = True

	def __init__(self):
		Source.__init__(self, _("Volume Control"))
	def get_items(self):
		yield Mute()
		yield UnMute()
		yield VolumeUp()
		yield VolumeDown()
		yield VolumeMax()
	def get_description(self):
		return __description__
	def get_icon_name(self):
		return "stock_volume"
	def provides(self):
		yield RunnableLeaf
