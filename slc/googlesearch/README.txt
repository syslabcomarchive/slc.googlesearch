SLC Googlesearch
================

Boilerplate
-----------

First, we must perform some setup.

    >>> from plone.testing.z2 import Browser
    >>> browser = Browser(layer['app'])
    >>> browser.handleErrors = False
    >>> portal = layer['portal']
    >>> portal_url = portal.absolute_url()

The following is useful when writing and debugging testbrowser tests. It lets
us see all error messages in the error_log.

    >>> portal.error_log._ignored_exceptions = ()

With that in place, we can go to the login form and log in.

    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = 'admin'
    >>> browser.getControl(name='__ac_password').value = 'secret'
    >>> browser.getControl(name='submit').click()

Here, we set the value of the fields on the login form and then simulate a
submit click.

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
	
