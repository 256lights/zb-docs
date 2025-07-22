```{eval-rst}
.. index:: binary cache
```

# Binary Cache Protocol

Because zb store objects are content-addressed, record their references,
and have a [fixed path](project:#path-algorithm),
they can be safely shared among machines.
Sharing store objects can speed up builds
or provide redundancy for network-dependent derivations (e.g. downloads).
To facilitate sharing, zb supports a binary cache protocol layered on top of [HTTP][RFC 9110] to fetch store objects.
This protocol is intended to be simple enough to be backed by a basic file server.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
"SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in [RFC 2119][].
[JSON][] structures are described using [JSON schema][].

[JSON]: https://datatracker.ietf.org/doc/html/rfc8259
[JSON schema]: https://json-schema.org/draft-07/draft-handrews-json-schema-01
[RFC 2119]: https://datatracker.ietf.org/doc/html/rfc2119
[RFC 9110]: https://datatracker.ietf.org/doc/html/rfc9110

```{toctree}
discovery
narinfo
nar-listings
realizations
```
