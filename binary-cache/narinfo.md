```{eval-rst}
.. index::
   .narinfo file
   binary cache; .narinfo file
```

# The `.narinfo` file format

Resources with the media type `text/x-nix-narinfo`
**MUST** conform to the syntax below.
(Syntax is defined in Augmented Backus-Naur Form as described in [RFC 5234][] and [RFC 7405][].)

```abnf
narinfo = *(key ": " value LF)

key   = *(%x01-09 / %x0B-30 / %x3B-FF)
        ; any UTF-8 code point except NUL, LF, or ':'
value = *(key / ":")
```

Keys not recognized by a client **MUST** be ignored.
Duplicate keys **SHOULD NOT** be present,
but if they are,
clients **MUST** only use the first value for a key.

Resources with the media type `text/x-nix-narinfo`
**SHOULD** conform to the stricter syntax below:

```abnf
narinfo-strict = store-path url compression nar-hash nar-size [references] ca

store-path  = %s"StorePath: " path LF
url         = %s"URL: " value LF
compression = %s"Compression: none" LF
nar-hash    = %s"NarHash: " hash LF
nar-size    = %s"NarSize: " 1*DIGIT LF
references  = %s"References:" 1*(" " path) LF
ca          = %s"CA: " ca-method ":" hash LF
ca-method   = %s"text" / %s"fixed" [ %s":r" ]

hash      = hash-algo ":" base32-value
hash-algo = %s"md5" / %s"sha1" / %s"sha256" / %s"sha512"

base32-value = 2*base32-digit
base32-digit = DIGIT / %x61-64 / %x66-6E / %x70-73 / %x76-7A
               ; lowercase alphanumeric except 'e', 'o', 't', or 'u'.
```

See the [store path syntax](project:#store-path-syntax) for the `path` rule.

[RFC 5234]: https://datatracker.ietf.org/doc/html/rfc5234
[RFC 7405]: https://datatracker.ietf.org/doc/html/rfc7405
