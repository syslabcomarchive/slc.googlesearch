from zope.component import getUtility 
from zope.formlib import form 
from plone.app.controlpanel.form import ControlPanelForm 
from slc.googlesearch.interfaces import IGoogleSearchSettings 
from slc.googlesearch import googlesearchMessageFactory as _

def osha_googlesearch_settings(context): 
    return getUtility(IGoogleSearchSettings) 

class SLCGoogleSearchControlPanel(ControlPanelForm): 

    form_fields = form.FormFields(IGoogleSearchSettings) 
    form_name = _(u"Google CSE settings") 
    label = _(u"Google CSE settings") 
    description = _(u"Please enter the appropriate connection settings" 
                      "for the CSE")

