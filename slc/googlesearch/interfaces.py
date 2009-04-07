from zope import schema
from zope.interface import Interface
from slc.googlesearch.browser.field import UIDLine

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers


from slc.googlesearch import googlesearchMessageFactory as _

class ICSELayer(Interface):
    """ Marker Interface used by BrowserLayer
    """


class IStoredCSETuple(Interface):
    label = schema.ASCIILine(title=_(u'Label'),
                        description=_('Give your search engine a label to identify it'),
                        default='',
                        required=True)
    
    cx = schema.ASCIILine(title=_(u"cx"), 
                   description=_(u"Paste the cx value that is used to identify your CSE"), 
                   default='', 
                   required=True) 
    
class IStoredCSESchema(Interface):
    stored_settings = schema.List(title=_(u"Stored CSE settings"),
                        description=_(u"Parameters to identify a stored CSE"),
                        default=[],
                        value_type=schema.Object(IStoredCSETuple, title=u"CSE parameters"),
                        required=False)


class ILinkedCSETuple(Interface):
    label = schema.ASCIILine(title=_(u'Label'),
                        description=_('Give your linked search engine a label to identify it'),
                        default='',
                        required=True)
    
    url = schema.ASCIILine(title=_(u"url"), 
                   description=_(u"Paste the URL that points to your stored search engine"), 
                   default='', 
                   required=True) 

class ILinkedCSESchema(Interface):
    linked_settings = schema.List(title=_(u"Linked CSE settings"),
                        description=_(u"Parameters to identify a linked CSE"),
                        default=[],
                        value_type=schema.Object(ILinkedCSETuple, title=u"CSE parameters"),
                        required=False)


class IGoogleSearchSettings(IStoredCSESchema, ILinkedCSESchema):
    """Combined schema for the adapter lookup.
    """


### Search URLS
# 
# 
class ISearchUrlTuple(Interface):
    url = schema.ASCIILine(title=_(u"url"), 
                   description=_(u"The URL that is to be included in the Search Engine"), 
                   default='', 
                   required=True)
    # for UIDs
    provider = UIDLine(title=_(u"provider"), 
                   description=_(u"The Provider where this URL comes from (if applicable)"), 
                   default='', 
                   required=False) 


class ISearchUrlSettings(Interface):
    """ Schema for holding a list of URLs that can be used to create a linked
        G-search.
    """
    urls = schema.List(title=_(u"URLs"),
                        description=_(u"Enter URLs you want to include in the linked CSE"),
                        default=[],
                        value_type=schema.Object(ISearchUrlTuple, title=u"URL parameters"),
                        required=False)
