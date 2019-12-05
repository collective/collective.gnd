# -*- coding: utf-8 -*-
from plone import api
from plone.app.upgrade.utils import loadMigrationProfile
import logging

log = logging.getLogger('collective.gnd.upgrades')


def reload_gs_profile(context):
    loadMigrationProfile(
        context,
        'profile-collective.gnd:default',
    )


def to_1002(context):
    # Reload GenericSetup profile
    reload_gs_profile(context)
    # AS we added gnd_id to metadata columns, we need to reindex all objects
    # with a gnd_id.
    brains = api.content.find(gnd_id={'query': 4, 'range': 'min'})
    log.info('Start reindexing index gnd_id on {} objects.'
             .format(len(brains)))
    for brain in brains:
        brain.getObject().reindexObject(idxs=['gnd_id'])
