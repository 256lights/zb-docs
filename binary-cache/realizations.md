```{eval-rst}
.. index:: binary cache; realization
```

# Realizations

Realization resources **SHOULD** use the media type `application/json`.
Realization documents **MUST** be in [JSON format][JSON]
and **MUST** conform to the [realization schema](schema/realization.json).

Realization documents **SHOULD** contain one or more realizations.
A realization is a mapping from derivation output to a store object.
Realization documents **SHOULD** have exactly one realization for each output of a derivation,
but **MAY** have more than one realization for a derivation output.

[JSON]: https://datatracker.ietf.org/doc/html/rfc8259

## Derivation Hashes

A realization is identified by its derivation's hash and an output name.
However, the `.drv` file's contents are not directly hashed.
To enable reuse of realizations
even if the input derivations have been modified but produce identical results,
the derivation hashes in a realization document are handled specially.

### Fixed Output Derivation Hashes

If a derivation is a fixed-output derivation,
then the hash is based on the fixed output hash and the store object path.
The exact structure of the hash algorithm input is defined by the following syntax:

```abnf
fixed-hash-input = %s"fixed:out:"
                   ca-method
                   hash-algo ":"
                   1*(2lower-hexdig) ":"
                   path

ca-method =  ""         ; flat file, hash by file contents
ca-method =/ %s"r:"     ; recursive file, hashed by NAR serialization
ca-method =/ %s"text:"  ; a text file, hashed by file contents

hash-algo    = %s"md5" / %s"sha1" / %s"sha256" / %s"sha512"
lower-hexdig = DIGIT / %s"a" / %s"b" / %s"c" / %s"d" / %s"e" / %s"f"
```

See the [store path syntax](project:#store-path-syntax) for the `path` rule.

### Floating Output Derivation Hashes

If a derivation is not a fixed-output derivation,
then the hash is a normalized version of the [`.drv` file format](project:#drv-format).
The following transformations are performed:

- The input derivations set is cleared.
- The input derivations' outputs are added to the input sources set.
- [Placeholders](project:#derivation-placeholders) are expanded in-place
  with the store paths used for the input derivations' outputs.

Then, the hash algorithm is given an input as defined by the following syntax:

```abnf
floating-hash-input = %s"floating:" drv-name ":" drv-file

drv-name = *(ALPHA / DIGIT / "+" / "-" / "." / "_" / "=")
```

See the [derivation specification](project:#drv-format) for the `drv-file` rule.

(realization-signatures)=
## Signatures

Each realization **SHOULD** include one or more signatures,
which provide a means for clients to authenticate
that a realization is trusted by a particular source.

The only defined signature format is `ed25519`.
(More formats may be added over time.)
Clients **MUST** ignore signatures with formats they do not support.
`ed25519` uses the [Ed25519 signature algorithm][].
The `publicKey` field is Base-64-encoded 32 bytes of a public key.
The `signature` field is Base-64-encoded 64 bytes of a signature.

The signature is computed for a JSON object encoded using the [JSON Canonicalization Scheme][RFC 8785].
The schema is defined by the `realizationForSignature` definition
in the realization JSON schema.
The reference classes in the object **MUST** be sorted by `path`,
then by `realization/derivationHash/algorithm`,
then by `realization/derivationHash/digest`,
then by `realization/outputName`.

[Ed25519 signature algorithm]: https://ed25519.cr.yp.to/
[RFC 8785]: https://datatracker.ietf.org/doc/html/rfc8785

## JSON Schema

```{literalinclude} schema/realization.json
:language: json
```
