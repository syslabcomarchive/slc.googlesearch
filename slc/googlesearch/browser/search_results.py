from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from slc.googlesearch.interfaces import IGoogleSearchSettings
from slc.googlesearch.browser.settings import AvailableCSEVocabularyFactory
from urllib import unquote


class SearchResultsView(BrowserView):
    """View for displaying Google CSE Search results
    """
    template = ViewPageTemplateFile('templates/search_results.pt')
    template.id = "slc_cse_search_results"
    
    
    def __call__(self):      
        qs = unquote(self.request.get('QUERY_STRING'))
        parts = qs.split('&')
        params = dict()
        for part in parts:
            try:
                key, val = part.split('=')
                params[key] = val
            except:
                # bungled or missing QS
                pass 
        if 'cx' not in params.keys() and 'cref' not in params.keys():
            cse = params.get('cse', None)
            if not cse:
                vocab = AvailableCSEVocabularyFactory(self)
                cse = len(vocab._terms) and vocab._terms[0].value or ''
                qs = "cse=%s" % cse

            if not cse:
                self.cse = ''
                return self.template()
            typus, value = cse.split('::')
            qs = qs+'&%s=%s' %(typus,value)
            url = "%s/%s?%s" % (self.context.absolute_url(), self.template.getId(), qs)
            self.request.RESPONSE.redirect(url)
        
        else:
            self.cse = self.request.get('cse', '')
            return self.template()

    def getCSE(self):
        return self.cse

    def getCx(self):
        typus, value = self.cse.split('::')
        if typus=='cx':
            return value
        return ''

    def getCref(self):
        typus, value = self.cse.split('::')
        if typus=='url':
            return value
        return ''

    def getCSEVocabulary(self):
        return AvailableCSEVocabularyFactory(self)

    def getQueryString(self):
        qs = self.request.get('QUERY_STRING')
        parts = qs.split('&')
        newparts = list()
        for part in parts:
            key, val = part.split('=')
            if key not in ('cse', 'cref', 'cx'):
                newparts.append(part)
       
        return '&'.join(newparts)