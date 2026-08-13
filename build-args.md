# Specifying What to Build

The arguments to `zb build` are either a list of paths/URLs,
or, if the `--expression` flag is passed, a [Lua](lua/index.md) expression.
Here are some examples of what's possible:

```shell
# Build what is returned from foo.lua.
zb build foo.lua
# Build what is stored in the global variable "myvar"
# in the file foo.lua.
zb build 'foo.lua#myvar'
# Build what is stored in the global variable "myvar"
# in the file foo.lua.
zb build --expression 'import("foo.lua").myvar'
# Fetch the file, evaluate it as Lua,
# and then build what it returns.
zb build https://www.example.com/foo.lua
# Fetch the zip file, unpack it,
# evaluate the file inside it called "foo.lua",
# then build what is stored in the global variable "myvar".
zb build 'https://www.example.com/archive.zip#foo.lua:myvar'
```

(output-values)=
## What Can Be Built

Most commonly, the objects that you will pass to `zb build`
will be objects returned by {lua:func}`derivation`.
A {term}`derivation` specifies a {term}`builder program` to run
and its dependencies, and `zb build` will arrange to run those.

`zb build` also accepts a few other types of objects:

- **Strings.** Because these carry [dependency information](lua/deps.md),
  `zb build` will build any derivation outputs referenced in the string
  before printing the full string to standard output.
- **Tables** or anything with the `__pairs` [metamethod][Metatables and Metamethods].
  Pair keys that are not strings or numbers are ignored.
  Pair values are converted via [`tostring`][] and are handled as above.
- Anything with the `__tostring` [metamethod][Metatables and Metamethods].
  The metamethod is called and the resulting string is handled as above.
  If a value has both a `__pairs` metamethod and a `__tostring` metamethod,
  then the `__tostring` metamethod is ignored.

```{eval-rst}
.. index:: __outputs metatable field
```

zb will use a zb-specific `__outputs` [metatable][Metatables and Metamethods] field if present.
{lua:func}`outputs` can be used to obtain the value from an `__outputs` metatable field in user-defined code.

```{include} outputs-metafield.md
```

(Objects returned by {lua:func}`derivation` have an `__outputs` field in their metatable,
so are not different from user-defined types.)

[`tostring`]: https://www.lua.org/manual/5.4/manual.html#pdf-tostring
[Metatables and Metamethods]: https://www.lua.org/manual/5.4/manual.html#2.4

```{eval-rst}
.. index:: URL
```

## URL Syntax

URL arguments to `zb build` comply with {rfc}`3986`
and can use any of the following {rfc}`schemes <3986#section-3.1>`:

- `file` (default if absent)
- `http`
- `https`
- `gs` ([Google Cloud Storage](https://docs.cloud.google.com/storage/docs/gsutil#syntax))

```{eval-rst}
.. index:: URL; fragment
```

The {rfc}`fragment <3986#section-3.5>` of a URL to `zb build` is split into two parts
at the last colon (`:`) that appears in the fragment.
Everything before the last colon is the *archive member*
and everything after the last colon is the *key path*.
If the fragment does not contain a colon,
then the entire fragment is the key path.
The presence of an archive member instructs zb to treat the file as an archive,
extract it using the same mechanism as in {lua:func}`extract`,
then use the file inside the archive with the same name.
If the key path is empty,
then the result of evaluating a URL is the same as the result of calling {lua:func}`await`
on the result of calling {lua:func}`import` with the path to the file as its argument.
Otherwise, the key path is a slash-separated sequence of [table indexes][Variables] on the module
(e.g. a key path of `foo/bar/baz` is equivalent to `foo.bar.baz` in Lua).

[Variables]: https://www.lua.org/manual/5.4/manual.html#3.2
