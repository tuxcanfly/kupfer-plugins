__kupfer_name__ = _("Pirate Bay Search")
__kupfer_actions__ = ("Search", )
__description__ = _("Search Pirate Bay with results shown directly")
__version__ = ""
__author__ = "Jakh Daven <tuxcanfly@gmail.com>"

from kupfer.objects import Action, Source
from kupfer.objects import TextLeaf, UrlLeaf

from tpb import TPB



SEARCH_HOST =  "http://pirateproxy.in"

class Search (Action):
	def __init__(self):
		Action.__init__(self, _("Pirate Bay Search"))

	def is_factory(self):
		return True
	def activate(self, leaf):
		return SearchResults(leaf.object)

	def item_types(self):
		yield TextLeaf

	def get_description(self):
		return __description__


class CustomDescriptionUrl (UrlLeaf):
	def __init__(self, obj, title, desc):
		UrlLeaf.__init__(self, obj, title)
		self.description = desc
	def get_description(self):
		return self.description

class SearchResults (Source):
	def __init__(self, query):
		Source.__init__(self, _('Results for "%s"') % query)
		self.query = query

	def repr_key(self):
		return self.query

	def get_items(self):
                api = TPB(SEARCH_HOST)
                results = api.search(self.query)
		for result in results:
			yield UrlLeaf(result.magnet_link, result.title)
		yield CustomDescriptionUrl(results.url,
				_('Show More Results For "%s"') % self.query,
				_("More results"))

	def provides(self):
		yield UrlLeaf

