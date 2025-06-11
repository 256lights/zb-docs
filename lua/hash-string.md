# Hash Strings

Certain zb functions take a *{index}`hash string`* argument.
Hash strings are the result of a [cryptographic hash function][]
and are used to ensure integrity of an output.
Hash strings are either in the format `<type>:<base16|base32|base64>`
or the [Subresource Integrity hash expression][] format `<type>-<base64>`,
where `<type>` is one of `md5`, `sha1`, `sha256`, or `sha512`.

[cryptographic hash function]: https://en.wikipedia.org/wiki/Cryptographic_hash_function
[Subresource Integrity hash expression]: https://www.w3.org/TR/SRI/#the-integrity-attribute
