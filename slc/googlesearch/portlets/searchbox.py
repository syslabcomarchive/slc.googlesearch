from Acquisition import aq_inner, aq_base
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements
from zope import schema

from plone.app.portlets.cache import render_cachekey
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from time import time
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from slc.googlesearch import googlesearchMessageFactory as _
from Products.CMFCore.utils import getToolByName
from slc.googlesearch.interfaces import IGoogleSearchSettings

class ICSEPortlet(IPortletDataProvider):
    selected_CSE = schema.Choice(title=_(u'Selected CSE'),
                    description=_('Pick the CSE you want to use for this search box'),
                    vocabulary="slc.googlesearch.vocabularies.AvailableCSE")
    

class Assignment(base.Assignment):
    implements(ICSEPortlet)

    def __init__(self, selected_CSE=''):
        self.selected_CSE = selected_CSE


    @property
    def title(self):
        return _(u"Google Searchbox")


class Renderer(base.Renderer):
    """Dynamically override standard header for search portlet"""
    _template = ViewPageTemplateFile('searchbox.pt')

    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)

        self.language = getToolByName(self.context, 'portal_languages').getPreferredLanguage()

        purl = getToolByName(self.context, 'portal_url')
        portal = purl.getPortalObject()
        self.portal_path = '/'.join(portal.getPhysicalPath())

    def _render_cachekey(method, self):
        preflang = getToolByName(self.context, 'portal_languages').getPreferredLanguage()
        return (preflang)
        
    # @ram.cache(_render_cachekey)
    def render(self):
        return xhtml_compress(self._template())

    def enable_livesearch(self):
        return False
        
    # def getCSE(self):
    #     return self.data.selected_CSE

    def getCx(self):
        typus, value = self.data.selected_CSE.split('::')
        if typus=='cx':
            return value
        return ''

    def getCref(self):
        typus, value = self.data.selected_CSE.split('::')
        if typus=='cref':
            return value
        return ''

    @memoize
    def _get_base_url(self):
        root = self.context.restrictedTraverse(self.portal_path)
        if hasattr(aq_base(aq_inner(root)), self.language):
            return '%s/%s' %(self.portal_path, self.language)
        else:
            return self.portal_path


    def search_action(self):
        base_url = self._get_base_url()
        return '%s/slc_cse_search_results' % base_url



class AddForm(base.AddForm):
    form_fields = form.Fields(ICSEPortlet)
    label = _(u"Add Google Search Portlet")
    description = _(u"This portlet shows a search box for the Google CSE.")

    def create(self, data):
        return Assignment(selected_CSE=data.get('selected_CSE', ''))


class EditForm(base.EditForm):
   form_fields = form.Fields(ICSEPortlet)
   label = _(u"Edit Google Search Portlet")
   description = _(u"This portlet shows a search box for the Google CSE.")
