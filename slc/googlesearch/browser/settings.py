from zope.component import getUtility 
from zope.interface import implements
from zope.formlib import form 

from plone.fieldsets.fieldsets import FormFieldsets
from plone.app.controlpanel.form import ControlPanelForm
from slc.googlesearch.interfaces import IGoogleSearchSettings 
from slc.googlesearch.interfaces import IStoredCSESchema, ILinkedCSESchema, IStoredCSETuple, ILinkedCSETuple
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from zope.app.form import CustomWidgetFactory
from zope.app.form.browser import ObjectWidget
from zope.app.form.browser import ListSequenceWidget
from persistent import Persistent
from zope.annotation.interfaces import IAnnotations

from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from zope.app.component.hooks import getSite

from slc.googlesearch import googlesearchMessageFactory as _

SETTING_KEY="slc.googlesearch.settings"


def slc_googlesearch_settings(context): 
    return getUtility(IGoogleSearchSettings) 

class StoredCSETuple:
    implements(IStoredCSETuple)
    
    def __init__(self, label='', cx=''):
        self.label = label
        self.cx = cx

class LinkedCSETuple:
    implements(ILinkedCSETuple)
    
    def __init__(self, label='', url=''):
        self.label = label
        self.url = url



class AvailableCSEVocabulary(object):
    """Vocabulary factory returning available CSE definitions
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        # need to get the context of the adapter
        site = getSite()
        GSS = getUtility(IGoogleSearchSettings)
        
        items = []
        # prefix value with the type of CSE
        for setting in GSS.stored_settings:
            value = "cx::%s" %(setting.cx)          
            items.append(SimpleTerm(value, value, setting.label))
        for setting in GSS.linked_settings:
            value = "cref::%s" %(setting.url)
            items.append(SimpleTerm(value, value, setting.label))
            
        return SimpleVocabulary(items)

AvailableCSEVocabularyFactory = AvailableCSEVocabulary()



class Settings(Persistent):
    """Settings for a site/subsite
    """
    stored_list = list()
    linked_list = list()


class GoogleSearchSettings(Persistent):
    implements(IGoogleSearchSettings)

    

    @apply
    def stored_settings():
        def get(self):
            return [StoredCSETuple(l,t) for (l,t) in self.settings.stored_list]
        def set(self, value):
            tuples = []
            for ta in value:
                label = ta.label
                cx = ta.cx
                tuples.append((label,cx))

            self.settings.stored_list = tuples
        return property(get, set)

    @apply
    def linked_settings():
        def get(self):
            return [LinkedCSETuple(l,t) for (l,t) in self.settings.linked_list]
        def set(self, value):
            tuples = []
            for ta in value:
                label = ta.label
                url = ta.url
                tuples.append((label,url))

            self.settings.linked_list = tuples
        return property(get, set)

    @property
    def settings(self):
        site = getSite()
        ann = IAnnotations(site)
        return ann.setdefault(SETTING_KEY, Settings())


stored_set = FormFieldsets(IStoredCSESchema)
stored_set.id = 'stored'
stored_set.label = _(u'Stored CSE')

linked_set = FormFieldsets(ILinkedCSESchema)
linked_set.id = 'linked'
linked_set.label = _(u'Linked CSE')

stored_settings_widget = CustomWidgetFactory(ObjectWidget, StoredCSETuple)
stored_widget = CustomWidgetFactory(ListSequenceWidget,
                                           subwidget=stored_settings_widget)

linked_settings_widget = CustomWidgetFactory(ObjectWidget, LinkedCSETuple)
linked_widget = CustomWidgetFactory(ListSequenceWidget,
                                           subwidget=linked_settings_widget)


class SLCGoogleSearchControlPanel(ControlPanelForm): 

    form_fields = FormFieldsets(stored_set, linked_set)
    form_fields['stored_settings'].custom_widget = stored_widget
    form_fields['linked_settings'].custom_widget = linked_widget
        

    form_name = _(u"Google CSE settings") 
    label = _(u"Google CSE settings") 
    description = _(u"Please enter the appropriate connection settings" 
                      "for the CSE")

