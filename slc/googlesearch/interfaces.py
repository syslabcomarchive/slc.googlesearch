from zope import schema
from zope.interface import Interface

from slc.googlesearch import googlesearchMessageFactory as _


class ICSELayer(Interface):
    """Marker Interface used by BrowserLayer"""


class IStoredCSETuple(Interface):
    label = schema.ASCIILine(
        title=_(u'Label'),
        description=_('Give your search engine a label to identify it'),
        default='',
        required=True)

    cx = schema.ASCIILine(
        title=_(u"cx"),
        description=_(u"Paste the cx value that is used to identify your CSE"),
        default='',
        required=True)


class IStoredCSESchema(Interface):
    stored_settings = schema.List(
        title=_(u"Stored CSE settings"),
        description=_(u"Parameters to identify a stored CSE"),
        default=[],
        value_type=schema.Object(IStoredCSETuple, title=u"CSE parameters"),
        required=False)


class ILinkedCSETuple(Interface):
    label = schema.ASCIILine(
        title=_(u'Label'),
        description=_('Give your linked search engine a label to identify it'),
        default='',
        required=True)

    url = schema.ASCIILine(
        title=_(u"url"),
        description=_(u"Paste the URL that points to your stored search "
                      "engine"),
        default='',
        required=True)


class ILinkedCSESchema(Interface):
    linked_settings = schema.List(
        title=_(u"Linked CSE settings"),
        description=_(u"Parameters to identify a linked CSE"),
        default=[],
        value_type=schema.Object(ILinkedCSETuple, title=u"CSE parameters"),
        required=False)


class IAdditionalParametersTuple(Interface):
    additional_query = schema.ASCIILine(
        title=_(u'Additional query'),
        description=_(u'Parameters that will be aded automatically to a '
                      'query'),
        default='',
        required=True)


class IAdditionalParametersSchema(Interface):
    additional_settings = schema.List(
        title=_(u"Additional parameters"),
        description=_(u"Additional parameters for the query"),
        default=[],
        value_type=schema.Object(IAdditionalParametersTuple,
                                 title=u"Additional parameters"),
        required=False)


class IGoogleSearchSettings(IStoredCSESchema, ILinkedCSESchema,
                            IAdditionalParametersSchema):
    """Combined schema for the adapter lookup."""
