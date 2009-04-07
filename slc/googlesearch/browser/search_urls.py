from zope.component import getUtility 
from zope.interface import implements
from zope.formlib import form
from zope.app.form import CustomWidgetFactory
from zope.app.form.browser import ObjectWidget
from zope.app.form.browser import ListSequenceWidget
from widget import UrlSequenceWidget
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from plone.fieldsets.fieldsets import FormFieldsets
from plone.app.controlpanel.form import ControlPanelForm
from slc.googlesearch.interfaces import ISearchUrlSettings, ISearchUrlTuple
from persistent import Persistent
from Products.Five import BrowserView
from Products.Archetypes.interfaces import IReferenceable
from Products.CMFCore.utils import getToolByName
from slc.googlesearch import googlesearchMessageFactory as _

def search_url_settings(context): 
    return getUtility(ISearchUrlSettings)
    
    
class SearchUrlTuple:
    implements(ISearchUrlTuple)
    
    def __init__(self, url='', provider=''):
        self.url = url
        self.provider = provider

class SearchUrlSettings(Persistent):
    implements(ISearchUrlSettings)
    
    url_list = list()

    @apply
    def urls():
        def get(self):
            return [SearchUrlTuple(l,t) for (l,t) in self.url_list]
        def set(self, value):
            tuples = []
            for ta in value:
                url = ta.url
                provider = ta.provider
                tuples.append((url,provider))

            self.url_list = tuples
        return property(get, set)


search_url_settings_widget = CustomWidgetFactory(ObjectWidget, SearchUrlTuple)
search_url_widget = CustomWidgetFactory(UrlSequenceWidget,
                                            subwidget=search_url_settings_widget)

class SearchUrlsControlPanel(ControlPanelForm): 

    # form_fields = FormFieldsets(stored_set, linked_set)
    form_fields = form.FormFields(ISearchUrlSettings)
    form_fields['urls'].custom_widget = search_url_widget
  

    form_name = _(u"Search URL settings") 
    label = _(u"Google CSE settings - search URLs") 
    description = _(u"Here you can enter and edit URLs that will be used for the linked CSE.")



class AddToSearchUrls(BrowserView):
    implements(ISearchUrlSettings)
    
    def __call__(self):
        context = self.context

        if IReferenceable.providedBy(context):
            uid = context.UID()
            util = getUtility(ISearchUrlSettings)
            urls = util.urls
            remoteUrl = context.getRemoteUrl()
            urls.append(SearchUrlTuple(remoteUrl, uid))
            util.urls = urls

            message = u'"%s" added to search urls' % unicode(context.title_or_id(), 'utf-8')
        else:
            message = u'"%s" could not be added to the search, because ist is not referenceable' % unicode(context.title_or_id(), 'utf-8')

        path = context.absolute_url()
        getToolByName(context, 'plone_utils').addPortalMessage(message)
        self.request.RESPONSE.redirect(path)