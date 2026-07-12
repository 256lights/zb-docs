```{eval-rst}
.. index:: binary cache; discovery document
```

# Discovery Document

Binary caches are typically referenced using a URL to a discovery document.
The discovery document **MUST** be a [JSON Hypertext Application Language][] (HAL) Document
and **SHOULD** be served with a media type of `application/hal+json`.

The following sections describe the link relation types
(as described in {rfc}`5988`)
used in the discovery document.

[JSON Hypertext Application Language]: https://datatracker.ietf.org/doc/html/draft-kelly-json-hal-11

## `https://zb-build.dev/api/rel/narinfo`

The `https://zb-build.dev/api/rel/narinfo` link relation type
defines how to look up the metadata for a store object.
Binary caches **SHOULD** provide this link in their discovery document.
If provided, the discovery document **MUST** use an array of links for this link relation type.
Each link **MUST** be a {rfc}`URI template <6570>`.

The defined template parameters for URIs of this link relation type are:

(narinfo-uri-template-parameters)=
`base`
: The store object's base file name.

`digest`
: The digest portion of the store object's base file name.

The linked resource **SHOULD** use the media type `text/x-nix-narinfo`.
The linked resource **MUST** follow the [`.narinfo` file format](narinfo.md).

## `https://zb-build.dev/api/rel/nar`

The `https://zb-build.dev/api/rel/nar` link relation type
defines where to `PUT` {term}`NAR` files when uploading to the binary cache.
(For downloading, the URL in a store object's [`.narinfo` file](narinfo.md) is the canonical link.)
Binary caches **MUST** provide this link if they support uploading.
If provided, the discovery document **MUST NOT** use an array for this link relation type.
The link **MUST** be a {rfc}`URI template <6570>`.

The defined template parameters for URIs of this link relation type are:

`base`
: The store object's base file name.

`digest`
: The digest portion of the store object's base file name.

The linked resource **SHOULD** use the media type `application/x-nix-nar`.

## `https://zb-build.dev/api/rel/narlisting`

The `https://zb-build.dev/api/rel/narlisting` link relation type
provides [NAR listings](nar-listings.md) for store objects.
Binary caches **MAY** provide this link in their discovery document
to support efficient access of individual files in the {term}`NAR` files.
If provided, the discovery document **MUST** use an array of links for this link relation type.
Each link **MUST** be a {rfc}`URI template <6570>`.
The URI template parameters are the same [as for `https://zb-build.dev/api/rel/narinfo`](project:#narinfo-uri-template-parameters).

## `https://zb-build.dev/api/rel/realization`

The `https://zb-build.dev/api/rel/realization` link relation type
provides mappings from derivation outputs to store objects.
Binary caches **SHOULD** provide this link in their discovery document.
If provided, the discovery document **MUST** use an array of links for this link relation type.
Each link **MUST** be a {rfc}`URI template <6570>`.

The defined template parameters for URIs of this link relation type are:

`hashAlgorithm`
: One of `md5`, `sha1`, `sha256`, or `sha512` depending on the hash.

`hashDigest`
: The hash bits encoded as lowercase hexadecimal.

The linked resource **SHOULD** use the media type `application/json`.
The resource **MUST** follow the [realization format](realizations.md).
