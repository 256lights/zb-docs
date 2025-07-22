# Store Paths

A store path is the absolute filesystem path of a {term}`store object`.
Store paths are based on the store object's contents.
This document specifies the restrictions on store object names
the restrictions on {term}`store directories <store directory>`,
and the algorithm for computing store paths.

```{eval-rst}
.. index:: store path; syntax
```

(store-path-syntax)=
## Syntax

The syntax of a store path in Augmented Backus-Naur Form (as described in [RFC 5234][])
is as follows:

```abnf
path = unix-path / windows-path

unix-path           =  *("/" unix-directory-part) "/" store-object-name
unix-directory-part =  ["."] (path-char / "\") *(path-char / "." / "\")
unix-directory-part =/ ".." 1*(path-char / "." / "\")

windows-path           =  windows-volume *("\" windows-directory-part) "\" store-object-name
windows-directory-part =  ["."] path-char *(path-char / ".")
windows-directory-part =/ ".." 1*(path-char / ".")
windows-volume         =  windows-drive-letter ":"
windows-volume         =/ "\" ["\."]                ; UNC
windows-volume         =/ "\??"                     ; Root Local Device path
windows-drive-letter   = %x01-2E / %30-5B / %5D-7F
                         ; CHAR except "/" or "\"

store-object-name      = 32(base32-digit) "-" 1*211(store-object-name-char)
store-object-name-char = ALPHA / DIGIT / "+" / "-" / "." / "_" / "="

path-char = ALPHA / DIGIT / "+" / "-" / "_" / "=" / "@" / %x80-FF
            ; characters that are always safe to use in file names

base32-digit = DIGIT / %x61-64 / %x66-6E / %x70-73 / %x76-7A
               ; lowercase alphanumeric except "e", "o", "t", or "u".
```

The 32 Base-32 digits at the beginning of a `store-object-name`
are referred to the {index}`store path's digest <store path; digest>`.
The characters after the first hyphen in a `store-object-name`
are referred to the {index}`store object's name <store object; name, store path; name>`.

[RFC 5234]: https://datatracker.ietf.org/doc/html/rfc5234

(path-algorithm)=
## Computing the Digest

Store paths are computed based on the contents of the store object.
There are three types of store objects for the purpose of computing a path:

- *Source* store objects are the most common:
  non-fixed derivation outputs
  and files imported into the store are source store objects.
  They can reference other store objects and themselves.
- *Text* store objects are used for [`.drv` files](project:#drv-format).
  They can reference other store objects, but not themselves.
  Text store objects **MUST** be a non-executable regular file.
- *Fixed-output store objects* are outputs of fixed-output derivations.
  They cannot contain references.

Once you know the type of store object,
the {term}`store directory`,
the store object's name,
and the store object's contents,
you can compute the store object's digest.
The process for computing the path is as follows:

1. Calculate the hash digest for the store object.

   - For a source store object,
     the hash digest **MUST** be the SHA-256 hash
     of the NAR serialization of the store object.

   - For a text store object,
     the hash digest **MUST** be a hash of the store object file's contents.
     One of the supported hash algorithms **MUST** be used,
     and **SHOULD** be SHA-256.

   - The hash digest for a fixed-output store object is a bit more involved.
     Given the output hash, the hash digest **MUST** be the SHA-256 hash
     of a string with the following syntax:

     ```abnf
     fixed-output-fingerprint = %s"fixed:out:" [%s"r:"] hash-algo ":" 1*(2lower-hexdig)

     hash-algo    = %s"md5" / %s"sha1" / %s"sha256" / %s"sha512"
     lower-hexdig = DIGIT / %s"a" / %s"b" / %s"c" / %s"d" / %s"e" / %s"f"
     ```

     `r:` is added if the fixed-output hash is computed
     from the NAR serialization of the store object.

2. Use the hash digest of the store object
   to produce a string with the following syntax:

   ```abnf
   fingerprint = store-path-type ":"
                 hash-algo ":"
                 1*(2lower-hexdig) ":"
                 store-directory ":"
                 1*211(store-object-name-char)
   store-path-type =  "source" *(":" path) [%s":self"]
                      ; Source store object
   store-path-type =/ "text" *(":" path)
                      ; Text store object
   store-path-type =/ "output:out"
                      ; Fixed-output store object

   store-directory   = unix-directory / windows-directory
   unix-directory    = "/" / 1*("/" unix-directory-part)
   windows-directory = windows-volume ("\" / 1*("\" windows-directory-part))

   hash-algo    = %s"md5" / %s"sha1" / %s"sha256" / %s"sha512"
   lower-hexdig = DIGIT / %s"a" / %s"b" / %s"c" / %s"d" / %s"e" / %s"f"
   ```

3. Compute the SHA-256 digest of the string from the previous step.

4. Build a 20-byte string based on the SHA-256 digest from the previous step.
   The first 12 bytes of the SHA-256 digest
   are XOR-ed with the last 12 bytes of the SHA-256 digest
   and then used as the first 12 bytes of the string.
   The last 8 bytes of the string
   are the 13th through 20th bytes of the SHA-256 digest.

5. The 20-byte string from the previous step
   is [Nix Base-32-encoded](https://edolstra.github.io/pubs/phd-thesis.pdf#page=97)
   to produce the store path digest.
