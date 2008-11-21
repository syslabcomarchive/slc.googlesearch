from persistent import Persistent 
from zope.interface import implements 
from slc.googlesearch.interfaces import IGoogleSearchSettings 

class GoogleSearchSettings(Persistent): 

    implements(IGoogleSearchSettings) 
    cx = ''


