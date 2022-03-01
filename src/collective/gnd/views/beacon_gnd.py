# -*- coding: utf-8 -*-
from collective.gnd.controlpanels.gnd_settings import IGndSettings
from datetime import datetime
from plone import api
from Products.Five.browser import BrowserView


class BeaconGnd(BrowserView):
    """Generates a plain textfile in Beacon format. See
    https://de.wikipedia.org/wiki/Wikipedia:BEACON/Format for more Details."""

    def __call__(self):
        self.portal = api.portal.get()
        self.portal_url = self.portal.absolute_url()
        self.render_all = api.portal.get_registry_record(
            name='render_all', interface=IGndSettings)
        self.portal_types = list(api.portal.get_registry_record(
            name='portal_types', interface=IGndSettings))
        self.message = api.portal.get_registry_record(
            name='message', interface=IGndSettings)
        self.contact = api.portal.get_registry_record(
            name='contact', interface=IGndSettings)
        self.institution = api.portal.get_registry_record(
            name='institution', interface=IGndSettings)
        self.description = api.portal.get_registry_record(
            name='description', interface=IGndSettings)
        self.request.response.setHeader('Content-Type',
                                        'text/plain')
        return self.gen_gnd_format()

    def get_gnd_ids(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        brains = []
        if self.render_all:
            if self.portal_types:
                brains = catalog.unrestrictedSearchResults(gnd_id={'query': '', 'range': 'min'}, portal_type=self.portal_types, sort_on='modified')
            else:
                brains = catalog.unrestrictedSearchResults(gnd_id={'query': '', 'range': 'min'}, sort_on='modified')

        else:
            # Returns only those IDs of objects accessable to the user
            if self.portal_types:
                brains = catalog(gnd_id={'query': '', 'range': 'min'}, portal_type=self.portal_types, sort_on='modified')
            else:
                brains = catalog(gnd_id={'query': '', 'range': 'min'}, sort_on='modified')

        self.ModificationDate = list(brains)[-1].ModificationDate
        result = [brain.gnd_id for brain in brains]
        return result

    def gen_gnd_format(self):
        gnd_ids = self.get_gnd_ids()
        # Build header
        content_dict = [
            u'#FORMAT: BEACON',
            u'#PREFIX: http://d-nb.info/gnd/',
            u'#LINK: http://www.w3.org/2000/01/rdf-schema#seeAlso',
            u'#TARGET: {0}/resolvegnd/{{ID}}'.format(self.portal_url),
            u'#MESSAGE: {0}'.format(self.message),
            u'#FEED: {0}/beacon-gnd.txt'.format(self.portal_url),
            u'#CONTACT: {0}'.format(self.contact),
            u'#INSTITUTION: {0}'.format(self.institution),
            u'#DESCRIPTION: {0}'.format(self.description),
            u'#TIMESTAMP: {0}'.format(self.ModificationDate),
            u'#UPDATE: always',
        ]
        # Get and add GND IDs to content
        content_dict.extend(gnd_ids)
        content = u'\n'.join(content_dict)
        return content
