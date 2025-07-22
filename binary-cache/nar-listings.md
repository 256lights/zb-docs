```{eval-rst}
.. index::
   .ls file
   NAR listing
   binary cache; NAR listing
```

# NAR listings

NAR listing resources describe the structure of a NAR file.
NAR listing resources **SHOULD** use the media type `application/json`.
The document **MUST** be in [JSON format][JSON]
and **MUST** conform to the [NAR listing schema](schema/nar-listing.json).
(This structure is the same as Nix's `.ls` files.)

Each filesystem object is represented as a JSON object with a `type` property.

- Regular files are `"type": "regular"`.
  Such objects have `executable`, `size`, and `narOffset` properties.
- Directories are `"type": "directory"`.
  Such objects have an `entries` property
  that is an object that maps names to other filesystem objects.
- Symbolic links (symlinks) are `"type": "symlink"`.
  Such objects have a `target` property.

A listing document is a JSON object with a `"version": 1` property
and a `root` property with a filesystem object value.

[JSON]: https://datatracker.ietf.org/doc/html/rfc8259

:::{rubric} JSON Schema
:heading-level: 2
:::

```{literalinclude} schema/nar-listing.json
:language: json
```
