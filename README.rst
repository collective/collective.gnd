.. image:: https://secure.travis-ci.org/collective/collective.gnd.png?branch=master
    :target: http://travis-ci.org/collective/collective.gnd

.. image:: https://coveralls.io/repos/github/collective/collective.gnd/badge.svg?branch=master
    :target: https://coveralls.io/github/collective/collective.gnd?branch=master
    :alt: Coveralls

.. image:: https://img.shields.io/pypi/l/collective.gnd.svg
    :target: https://pypi.python.org/pypi/collective.gnd/
    :alt: License

.. image:: https://badges.gitter.im/collective/collective.gnd.svg
   :alt: Join the chat at https://gitter.im/collective/collective.gnd
   :target: https://gitter.im/collective/collective.gnd?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge


==============
collective.gnd
==============

Plone addon which provides a `GND ID <https://www.wikidata.org/wiki/Property:P227>`_ resolver and a `BEACON <http://gbv.github.io/beaconspec/>`_ API.

Features
--------

- GND ID resolver: ``/resolvegnd/08151111``
- GND ID Behavior, which provides a ``gnd_id`` field
- Provides a ``gnd_id`` index
- BEACON API (BEACON List): /beacon-gnd.txt


Installation
------------

Install collective.gnd by adding it to your buildout::

    [buildout]

    ...

    eggs =
        collective.gnd


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/collective/collective.gnd/issues
- Source Code: https://github.com/collective/collective.gnd


License
-------

The project is licensed under the GPLv2.
