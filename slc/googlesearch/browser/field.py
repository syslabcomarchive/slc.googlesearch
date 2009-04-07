from zope.schema.interfaces import IASCIILine
from zope.schema._field import ASCIILine
from zope.interface import implements

class IUIDLine(IASCIILine):
    u"""Field containing a UID."""

class UIDLine(ASCIILine):
    """A field that holds a UID"""
    implements(IUIDLine)