SLC Googlesearch
================

Boilerplate
-----------

This is a full-blown functional test. The emphasis here is on testing what
the user may input and see, and the system is largely tested as a black box.
We use PloneTestCase to set up this test as well, so we have a full Plone site
to play with. We *can* inspect the state of the portal, e.g. using 
self.portal and self.folder, but it is often frowned upon since you are not
treating the system as a black box. Also, if you, for example, log in or set
roles using calls like self.setRoles(), these are not reflected in the test
browser, which runs as a separate session.

Being a doctest, we can tell a story here.

First, we must perform some setup. We use the testbrowser that is shipped
with Five, as this provides proper Zope 2 integration. Most of the 
documentation, though, is in the underlying zope.testbrower package.

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()

The following is useful when writing and debugging testbrowser tests. It lets
us see all error messages in the error_log.

    >>> self.portal.error_log._ignored_exceptions = ()

With that in place, we can go to the portal front page and log in. We will
do this using the default user from PloneTestCase:

    >>> from Products.PloneTestCase.setup import portal_owner, default_password

    >>> browser.open(portal_url)

We have the login portlet, so let's use that.

    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()

Here, we set the value of the fields on the login form and then simulate a
submit click.

We then test that we are still on the portal front page:

    >>> browser.url == portal_url
    True

And we ensure that we get the friendly logged-in message:

    >>> "You are now logged in" in browser.contents
    True



Adding basic settings
---------------------
	
We navigate to the Googlesearch controlpanel.

	>>> browser.getLink('Site Setup').click()
	>>> browser.getLink('Google Custom Search').click()
	>>> "Google CSE settings" in browser.contents
	True
	
There are no CSE settings yet.

	>>> "CSE parameters" in browser.contents
	False
	
Therefore we add some:

	>>> browser.getControl('Add Stored CSE settings').click()
	>>> browser.getControl(name="form.stored_settings.0.label").value = "My custom search"
	>>> browser.getControl(name="form.stored_settings.0.cx").value = "012345"
	>>> browser.getControl('Save').click()
	>>> "Changes saved" in browser.contents	
	True
	
The parameters are present in the form.

	>>> "My custom search" in browser.contents
	True

Now we add linked settings:

	>>> browser.getControl('Add Linked CSE settings').click()
	>>> browser.getControl(name="form.linked_settings.0.label").value = "My linked search2"
	>>> browser.getControl(name="form.linked_settings.0.url").value = "http://nohost/googleCSE"
	>>> browser.getControl('Save').click()	
	>>> "Changes saved" in browser.contents
	True

And they are also present in the form now.

	>>> "My linked search" in browser.contents
	True

And the stored CSE is still there.

	>>> "My custom search" in browser.contents
	True

Adding the portlet
-------------------

Now let's go back to the homepage and add a Googlesearch portlet.

	>>> browser.getLink('Home').click()
	>>> browser.getLink('Manage portlets').click()
	>>> browser.open('/'.join(browser.url.split('/')[:-1] + ['++contextportlets++plone.leftcolumn', '+', 'slc.GoogleSearchBox']))
	>>> "Add Google Search Portlet" in browser.contents
	True

The drop-down for the selected CSE must contain our 2 previously defined CSEs.

	>>> 'cx::012345' in browser.getControl(name='form.selected_CSE').options	
	True
	
	>>> 'cref::http://nohost/googleCSE' in browser.getControl(name='form.selected_CSE').options
	True

And so we add the portlet.

	>>> browser.getControl(name='form.selected_CSE').value = ['cx::012345']
	>>> browser.getControl('Save').click()
	>>> "Google Searchbox" in browser.contents
	True
	
