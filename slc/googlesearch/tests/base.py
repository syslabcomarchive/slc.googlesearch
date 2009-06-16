from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from Products.PloneTestCase import layer

SiteLayer = layer.PloneSite

class SLCSGooglesearchLayer(SiteLayer):
    @classmethod
    def setUp(cls):
        """Set up additional products and ZCML required to test this product.
        """
        ztc.installPackage('slc.googlesearch')
        ptc.setupPloneSite(products=['slc.googlesearch'])

        # Load the ZCML configuration for this package and its dependencies

        fiveconfigure.debug_mode = True
        import slc.googlesearch
        zcml.load_config('configure.zcml', slc.googlesearch)
        fiveconfigure.debug_mode = False

        
        SiteLayer.setUp()

# The order here is important: We first call the deferred function and then 
# let PloneTestCase install it during Plone site setup

class TestCase(ptc.PloneTestCase):
    """Base class used for test cases
    """
    layer = SLCSGooglesearchLayer

class FunctionalTestCase(ptc.FunctionalTestCase):
    """Test case class used for functional (doc-)tests
    """
    layer = SLCSGooglesearchLayer
