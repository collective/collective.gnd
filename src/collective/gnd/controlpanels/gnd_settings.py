# -*- coding: utf-8 -*-
from collective.gnd import _
from plone.app.registry.browser import controlpanel
from plone.z3cform import layout
from zope import schema
from zope.interface import Interface


class IGndSettings(Interface):
    """ Define settings data structure for registry"""

    message = schema.TextLine(
        title=_(u'Message'),
        description=_(u''),
        default=u'My Portal',
        required=False,
        readonly=False,
    )

    contact = schema.TextLine(
        title=_(u'Contact'),
        description=_(u''),
        default=u'firstname lastname <jane@example.com>',
        required=False,
        readonly=False,
    )

    institution = schema.TextLine(
        title=_(u'Institution'),
        description=_(u''),
        default=u'',
        required=False,
        readonly=False,
    )

    description = schema.TextLine(
        title=_(u'Description'),
        description=_(u''),
        default=u'',
        required=False,
        readonly=False,
    )

    portal_types = schema.Set(
        title=_(u'Types to include in beacon list'),
        description=_(u'Select the types for which the beacon list shall be rendered. If nothing selected, beacon list will contain all objects with gnd id'),
        value_type=schema.Choice(
            vocabulary='plone.app.vocabularies.UserFriendlyTypes',
        ),
        required=False,
        readonly=False)

    render_all = schema.Bool(
        title=_(u'Render all?'),
        description=_(u'If enabled, all indexed GND-IDs will be listed in '
                      u'beacon-gnd.txt, wether the target object is accessable'
                      u' or not. Disable this to ensure security settings '
                      u' are considered.'),
        default=False,
        required=False,
        readonly=False,
    )

    resolver_base_url = schema.URI(
        title=_(u'Resolver base URL'),
        description=_(u'If a resolver base URL is specified, the gnd_resolver '
                      u'service uses this instead of the portal base URL to '
                      u'build the redirect target URL, e.g. '
                      u'[http://base.url][/relative/path/to/object]'),
        required=False,
        readonly=False,
    )


class GndSettingsEditForm(controlpanel.RegistryEditForm):
    """
    """

    schema = IGndSettings
    label = u'GND Settings'


GndSettingsView = layout.wrap_form(
    GndSettingsEditForm, controlpanel.ControlPanelFormWrapper)
