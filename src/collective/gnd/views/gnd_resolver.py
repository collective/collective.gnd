# -*- coding: utf-8 -*-
from collective.gnd.controlpanels.gnd_settings import IGndSettings
from plone import api
from Products.Five.browser import BrowserView
from zExceptions import NotFound
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


@implementer(IPublishTraverse)
class GndResolver(BrowserView):
    """Resolves a GND-ID from URL.
    """

    subpath = None

    def gndToURL(self):
        """Resolves a GND-ID to a URL via the gnd_id index of portal_catalog.
        """
        catalog = api.portal.get_tool('portal_catalog')
        res = catalog.unrestrictedSearchResults(gnd_id=self.gnd)
        if res:
            return res[0].getURL()

    def publishTraverse(self, request, name):
        self.gnd = name
        traverse_subpath = self.request['TraversalRequestNameStack']
        if traverse_subpath:
            traverse_subpath = list(traverse_subpath)
            traverse_subpath.reverse()
            self.subpath = traverse_subpath
            self.request['TraversalRequestNameStack'] = []
        return self

    def __call__(self):
        url = self.gndToURL()
        resolver_base_url = api.portal.get_registry_record(
            'resolver_base_url',
            interface=IGndSettings)
        # TBD: Ensure resolver base URL contains protocol, e.g. https://,
        # otherwise redirects will not work
        portal_url = api.portal.get().absolute_url()

        if not url:
            raise NotFound('There is no resource available with the specified '
                           'GND-Identifier.')
        # Add possible sub path
        if self.subpath:
            url = '/'.join([url] + self.subpath)
        # Add possible query params
        if self.request.QUERY_STRING:
            url += '?' + self.request.QUERY_STRING
        # Replace base URL if given
        if resolver_base_url:
            url = url.replace(portal_url, resolver_base_url)
        return self.request.response.redirect(url, status=301)
