# Hash Strings

Certain zb functions take a *{index}`hash string`* argument.
Hash strings are the result of a [cryptographic hash function][]
and are used to ensure integrity of an output.

Examples include:

- `sha256:ee4c78f4b1915c7dafb0d55e8cd6f20fe82396a21a6ab2add9bb879fb9301bc2`
- `sha1:da39a3ee5e6b4b0d3255bfef95601890afd80709`
- `sha256-7kx49LGRXH2vsNVejNbyD+gjlqIaarKt2buHn7kwG8I=`

[cryptographic hash function]: https://en.wikipedia.org/wiki/Cryptographic_hash_function

:::{rubric} Syntax
:heading-level: 2
:::

The syntax of a hash string in Augmented Backus-Naur Form (as described in [RFC 5234][] and  [RFC 7405][])
is as follows:

```abnf
hash-string = hash-algo ":" (base16-value / base32-value / base64-value)
              / sri
sri = hash-algo "-" base64-value

hash-algo = %s"md5" / %s"sha1" / %s"sha256" / %s"sha512"

base16-value = 1*(2HEXDIG)

base32-value = 2*base32-digit
base32-digit = DIGIT / %x61-64 / %x66-6E / %x70-73 / %x76-7A
               ; lowercase alphanumeric except "e", "o", "t", or "u".

base64-value = *(4base64-digit) 2base64-digit (2base64-digit / (base64-digit / "=") "=")
base64-digit = ALPHA / DIGIT / "+" / "/"
```

The `sri` rule is a strict subset of a [Subresource Integrity hash expression][].

[RFC 5234]: https://datatracker.ietf.org/doc/html/rfc5234
[RFC 7405]: https://datatracker.ietf.org/doc/html/rfc7405
[Subresource Integrity hash expression]: https://www.w3.org/TR/SRI/#the-integrity-attribute
