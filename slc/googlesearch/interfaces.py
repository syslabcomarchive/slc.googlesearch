from zope import schema
from zope.interface import Interface

from zope.app.container.constraints import contains
from zope.app.container.constraints import containers

from slc.googlesearch import googlesearchMessageFactory as _

class ICSELayer(Interface):
    """ Marker Interface used by BrowserLayer
    """

class IGoogleSearchSettings(Interface):
    """ Settings to access the RDBMS """
    cx = schema.ASCIILine(title=_(u"cx"), 
                   description=_(u"Paste cx value, used to identify your CSE"), 
                   default='', 
                   required=True) 
