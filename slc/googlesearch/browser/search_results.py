from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

class SearchResultsView(BrowserView):
    """View for displaying Google CSE Search results
    """
    template = ViewPageTemplateFile('templates/search_results.pt')
    template.id = "faq_view"
    
    def __call__(self):
        self.request.set('disable_border', True)
        return self.template()
