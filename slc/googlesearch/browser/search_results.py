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
        
        # if a CSE value is present, invalidate cx and cref, because we are switching source;
        # but only if the cse value differs from the current selection
        if params.has_key('cse'):
            cse = params.get('cse')
            del params['cse']
            typus, value = cse.split('::')
            if params.has_key('cx') and not params.get('cx', '')==value:
                del params['cx']
            if params.has_key('cref') and not params.get('cref', '')==value:
                del params['cref']
        else:
            cse = ''
        
        # if neither cx nor cref are available as parameters, extract them from cse
        # and redirect with the proper query-string
        if 'cx' not in params.keys() and 'cref' not in params.keys():
            # If there is no CSE value (page called without params),
            # get the first defined CSE from the vocabulary of CSEs
            if not cse:
                vocab = AvailableCSEVocabularyFactory(self)
                cse = len(vocab._terms) and vocab._terms[0].value or ''
            
            # if no CSE is found in the vocabulary, show blank template
            if not cse:
                self.cx = self.cref = ''
                return self.template()
            qsparts = list()
            for key, value in params.items():
                qsparts.append('%s=%s' %(key, value))
            qs = '&'.join(qsparts)
            typus, value = cse.split('::')
            qs = qs + '&%s=%s' %(typus,value)
            url = "%s/%s?%s" % (self.context.absolute_url(), self.template.getId(), qs)
            self.request.RESPONSE.redirect(url)
        
        # we have a valid query-string; save cx and cref values, and display template
        else:
            self.cx = params.get('cx', '')
            self.cref = params.get('cref', '')
            return self.template()
    
    
    def getCx(self):
        return self.cx
    
    def getCref(self):
        return self.cref
    
    
    def getAvailableCSE(self):
        vocab = AvailableCSEVocabularyFactory(self)
        cse = list()
        for term in vocab:
            typus, realvalue = term.value.split('::')
            stored_value = getattr(self, typus, '')
            cse.append(dict(
                title = term.title,
                value = term.value,
                checked = stored_value==realvalue and 'checked' or ''))
        return cse

    def getSelectedCSE(self):
        vocab = AvailableCSEVocabularyFactory(self)
        # try cx first
        val = "cx::%s" % self.getCx()
        title = vocab.by_value.get(val) and vocab.by_value.get(val).title or ''
        if not title:
            val = "cref::%s" % self.getCref()
            title = vocab.by_value.get(val) and vocab.by_value.get(val).title or ''
        return title
        