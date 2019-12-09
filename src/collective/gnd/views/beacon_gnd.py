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
        if self.render_all:
            # Returns all indexed IDs without security check
            index = catalog._catalog.getIndex('gnd_id')
            return [id for id in index._index if id]
        else:
            # Returns only those IDs of objects accessable to the user
            brains = catalog(gnd_id={'query': 4, 'range': 'min'},
                             sort_on='gnd_id')
            return [brain.gnd_id for brain in brains]

    def gen_gnd_format(self):
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
            u'#TIMESTAMP: {0}'.format(datetime.now()),
            u'#UPDATE: always',
        ]
        # Get and add GND IDs to content
        gnd_ids = self.get_gnd_ids()
        content_dict.extend(gnd_ids)
        content = u'\n'.join(content_dict)
        return content
