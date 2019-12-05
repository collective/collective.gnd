# -*- coding: utf-8 -*-

from collective.gnd.controlpanels.gnd_settings import IGndSettings
from plone import api
from plone.registry.interfaces import IRegistry
from Products.Five.browser import BrowserView
from zope.component import getUtility
from datetime import datetime


class BeaconGnd(BrowserView):

    def __call__(self):
        self.portal = api.portal.get()
        self.portal_url = self.portal.absolute_url()
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(IGndSettings)
        self.request.response.setHeader('Content-Type',
                                        'text/plain')
        return self.gen_gnd_format()

    def get_gnd_ids(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        if self.settings.render_all:
            # returns all indexed IDs without security check
            index = catalog._catalog.getIndex('gnd_id')
            return [id for id in index._index if id]
        else:
            # returns only those IDs of objects accessable to the user
            brains = catalog(gnd_id={'query': 4, 'range': 'min'},
                             sort_on='gnd_id')
            return [brain.gnd_id for brain in brains]

    def gen_gnd_format(self):
        header_lines = []
        header_lines.append(u'#FORMAT: BEACON')
        header_lines.append(u'#PREFIX: http://d-nb.info/gnd/')
        header_lines.append(u'#LINK: http://www.w3.org/2000/01/rdf-schema#seeAlso')
        header_lines.append(u'#TARGET: {0}/resolvegnd/{{ID}}'.format(self.portal_url))
        header_lines.append(u'#MESSAGE: {0}'.format(self.settings.message))
        header_lines.append(u'#FEED: {0}/beacon-gnd.txt'.format(self.portal_url))
        header_lines.append(u'#CONTACT: {0}'.format(self.settings.contact))
        header_lines.append(u'#INSTITUTION: {0}'.format(self.settings.institution))
        header_lines.append(u'#DESCRIPTION: {0}'.format(self.settings.description))
        header_lines.append(u'#TIMESTAMP: {0}'.format(datetime.now()))
        header_lines.append(u'#UPDATE: always')
        gnd_ids = self.get_gnd_ids()
        header_lines.extend(gnd_ids)
        header = u'\n'.join(header_lines)
        return header
