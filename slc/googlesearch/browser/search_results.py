from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from slc.googlesearch.interfaces import IGoogleSearchSettings

class SearchResultsView(BrowserView):
    """View for displaying Google CSE Search results
    """
    template = ViewPageTemplateFile('templates/search_results.pt')
    
    def __call__(self):
        self.request.set('disable_border', True)
        purl = getToolByName(self.context, 'portal_url')
        portal = purl.getPortalObject()
        self.settings = IGoogleSearchSettings(portal)
        return self.template()

    def getCx(self):
        return getattr(self.settings, 'cx', '')
