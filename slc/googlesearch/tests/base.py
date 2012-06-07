from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.testing import z2


class SLCGoogleSearch(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import slc.googlesearch
        self.loadZCML('configure.zcml', package=slc.googlesearch)

        z2.installProduct(app, 'slc.googlesearch')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'slc.googlesearch:default')

    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'slc.googlesearch')


SLCGOOGLESEARCH_FIXTURE = SLCGoogleSearch()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(SLCGOOGLESEARCH_FIXTURE,),
    name="SLCGoogleSearch:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(SLCGOOGLESEARCH_FIXTURE,),
    name="SLCGoogleSearch:Functional")
