from zope.app.form.browser.textwidgets import ASCIIWidget
from zope.app.form.browser.sequencewidget import ListSequenceWidget
from Products.CMFCore.utils import getToolByName
from zope.app.component.hooks import getSite
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile


class UIDWidget(ASCIIWidget):
    
    __call__ = ViewPageTemplateFile('widget.pt')
    
    def _getFormValue(self):
        site = getSite()
        pc = getToolByName(site, 'portal_catalog')
        value = self._data
        brains = pc(UID=value)
        input_value = len(brains) and brains[0].getURL() or 'nixn'
        if len(brains):
            return dict(url=brains[0].getURL(), title=brains[0].Title, value=value)
        
        return dict(url='', title='', value=value)

class UrlSequenceWidget(ListSequenceWidget):
    template = ViewPageTemplateFile('urlsequencewidget.pt')