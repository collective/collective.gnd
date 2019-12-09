Changelog
=========

1.1 (unreleased)
----------------

- Added configurable, security related rendering of BEACON file. If registry record render_all is False, only GND-IDs, which are accessable by the requesting user are listed in the BEACON file. Otherwise all indexed values are listed.
  [ukretschmer]
- Gnd resolver service now has configurable base URL, which allows redirecting to targets with another base URL but the same object path.
  [ukretschmer]

1.0 (2019-08-26)
----------------

- Fix default in gnd_id property in behavior
  [MrTango]


1.0b2 (2019-06-20)
------------------

- Fix target (gnd resolver) URL in BEACON file
  [MrTango]


1.0b1 (2019-06-20)
------------------

- prevent None entries in gnd_ids
  [MrTango]


1.0a2 (2019-06-20)
------------------

- Fix README RST syntax
  [MrTango]

1.0a1 (2019-06-20)
------------------

- Initial release.
  [MrTango]
