from zope.component import getUtility
from zope.interface import implements
from zope.formlib import form

from plone.fieldsets.fieldsets import FormFieldsets
from plone.app.controlpanel.form import ControlPanelForm
from slc.googlesearch.interfaces import IGoogleSearchSettings
from slc.googlesearch.interfaces import IStoredCSESchema, ILinkedCSESchema, IStoredCSETuple, ILinkedCSETuple, IAdditionalParametersTuple, IAdditionalParametersSchema
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
from Products.CMFPlone.interfaces import IPloneSiteRoot

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

class AdditionalParametersTuple:
    implements(IAdditionalParametersTuple)

    def __init__(self, additional_query=''):
        self.additional_query = additional_query


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
    additionals_list = list()


class GoogleSearchSettings(Persistent):
    implements(IGoogleSearchSettings)
    
    # keep a "backup" copy
    # dirty hack, since getSite can return an Products.Five.metaclass.FormlibValidation instance,
    # which cannot be used for IAnnotation...
    stored_list = list()
    linked_list = list()
    additionals_list = list()
    
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
            self.stored_list = tuples
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
            self.linked_list = tuples
        return property(get, set)

    @apply
    def additional_settings():
        def get(self):
            return [AdditionalParametersTuple(q,) for (q,) in self.settings.additionals_list]
        def set(self, value):
            tuples = []
            for ta in value:
                additional_query = ta.additional_query
                tuples.append((additional_query,))
            self.settings.additionals_list = tuples
            self.additionals_list = tuples
        return property(get, set)
   
    @property
    def settings(self):
        site = getSite()
        if not IPloneSiteRoot.providedBy(site):
            # here be dirty hack
            dummy = Settings()
            dummy.stored_list = self.stored_list
            dummy.linked_list = self.linked_list
            dummy.additionals_list = self.additionals_list
            return dummy
        ann = IAnnotations(site)
        return ann.setdefault(SETTING_KEY, Settings())


stored_set = FormFieldsets(IStoredCSESchema)
stored_set.id = 'stored'
stored_set.label = _(u'Stored CSE')

linked_set = FormFieldsets(ILinkedCSESchema)
linked_set.id = 'linked'
linked_set.label = _(u'Linked CSE')

additional_set = FormFieldsets(IAdditionalParametersSchema)
additional_set.id = 'additional'
additional_set.label = 'Additional parameters'

stored_settings_widget = CustomWidgetFactory(ObjectWidget, StoredCSETuple)
stored_widget = CustomWidgetFactory(ListSequenceWidget,
                                           subwidget=stored_settings_widget)

linked_settings_widget = CustomWidgetFactory(ObjectWidget, LinkedCSETuple)
linked_widget = CustomWidgetFactory(ListSequenceWidget,
                                           subwidget=linked_settings_widget)

additional_parameters_widget = CustomWidgetFactory(ObjectWidget, AdditionalParametersTuple)
additional_widget = CustomWidgetFactory(ListSequenceWidget,
                                           subwidget=additional_parameters_widget)


class SLCGoogleSearchControlPanel(ControlPanelForm):
    
    form_fields = FormFieldsets(stored_set, linked_set, additional_set)
    form_fields['stored_settings'].custom_widget = stored_widget
    form_fields['linked_settings'].custom_widget = linked_widget
    form_fields['additional_settings'].custom_widget = additional_widget

    
    form_name = _(u"Google CSE settings")
    label = _(u"Google CSE settings")
    description = _(u"Please enter the appropriate connection settings"
                      "for the CSE")

