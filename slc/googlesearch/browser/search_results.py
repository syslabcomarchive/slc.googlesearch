from Acquisition import aq_inner, aq_base
from plone.memoize.instance import memoize
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from slc.googlesearch.browser.settings import AvailableCSEVocabularyFactory
from slc.googlesearch.config import RESULTS_INTRO_PAGE_NAME
from urllib import unquote


class SearchResultsLinkedView(BrowserView):
    """View for displaying Google CSE Search results"""

    def __call__(self):
        self.language = getToolByName(self.context,
            'portal_languages').getPreferredLanguage()

        purl = getToolByName(self.context, 'portal_url')
        portal = purl.getPortalObject()
        self.portal_path = '/'.join(portal.getPhysicalPath())
        self.cx = self.cref = ''

        vocab = AvailableCSEVocabularyFactory(self)
        for term in vocab._terms:
            typus, value = term.value.split('::')
            if typus == 'cx':
                self.cx = value
            elif typus == 'cref':
                self.cref = value

        return self.index()

    @memoize
    def _get_base(self):
        root = self.context.restrictedTraverse(self.portal_path)
        if hasattr(aq_base(aq_inner(root)), self.language):
            return getattr(root, self.language).getCanonical()
        else:
            return root

    def getCx(self):
        return self.cx

    def getCref(self):
        return self.cref


    def getSelectedCSE(self):
        vocab = AvailableCSEVocabularyFactory(self)
        # try cref first
        val = "cref::%s" % self.getCref()
        title = vocab.by_value.get(val) and vocab.by_value.get(val).title or ''
        if not title:
            val = "cx::%s" % self.getCx()
            title = (vocab.by_value.get(val) and vocab.by_value.get(val).title
                     or '')
        return title

    def getIntroDocument(self):
        base = self._get_base()

        if getattr(aq_base(base), RESULTS_INTRO_PAGE_NAME, None):
            intro = getattr(base, RESULTS_INTRO_PAGE_NAME)
            intro = intro.getTranslation(self.language) or intro
            return intro

        return None


class SearchResultsSEView(SearchResultsLinkedView):

    def getSelectedCSE(self):
        vocab = AvailableCSEVocabularyFactory(self)
        # try cx first
        val = "cx::%s" % self.getCx()
        title = vocab.by_value.get(val) and vocab.by_value.get(val).title or ''
        if not title:
            val = "cref::%s" % self.getCref()
            title = (vocab.by_value.get(val) and vocab.by_value.get(val).title
                     or '')
        return title