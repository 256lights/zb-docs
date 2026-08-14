# Specifying What to Build

The arguments to `zb build` are either a list of paths/URLs,
or, if the `--expression` flag is passed, a [Lua](lua/index.md) expression.
Here are some examples:

```shell
# Build what is returned from the Lua file at foo/bar.lua.
zb build foo/bar.lua
zb build --expression 'await(import("foo/bar.lua"))'

# Build what is stored in the global variable "myvar"
# in the Lua file at foo/bar.lua.
zb build 'foo/bar.lua#myvar'
zb build --expression 'import("foo/bar.lua").myvar'

# Build what is stored in the field "field"
# in the global table "myvar"
# in the Lua file at foo/bar.lua.
zb build 'foo/bar.lua#myvar/field'
zb build --expression 'import("foo/bar.lua").myvar.field'

# Download the file at https://www.example.com/foo.lua,
# evaluate it as Lua,
# and then build what is stored in the global variable "myvar".
zb build 'https://www.example.com/foo.lua#myvar'

# Download the zip file at https://www.example.com/archive.zip,
# unpack it,
# evaluate the Lua file inside it called "foo.lua",
# then build what is stored in the global variable "myvar".
zb build 'https://www.example.com/archive.zip#foo.lua:myvar'
```

```{eval-rst}
.. index:: URL
```

## URL Syntax

URL arguments to `zb build` can use any of the following {rfc}`schemes <3986#section-3.1>`:

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

(output-eval)=
## What Can Be Built

Once `zb build` has evaluated the Lua value from an expression or a URL,
`zb build` converts the value to a string using [`tostring`][],
unless the value is a table.
Because strings carry [dependency information](lua/deps.md),
`zb build` will build any {term}`derivation` outputs referenced in the string
before printing the full string to standard output.
If the Lua value is a table, the table will be walked using [`pairs`][].
Pairs with keys that are not strings or numbers will be ignored.
Each value will be converted to a string using [`tostring`][].

```{eval-rst}
.. index:: __outputs metatable field
```

```{include} outputs-metafield.md
```

:::{seealso}

{lua:func}`outputs`
: Built-in function to obtain a value's outputs in user-defined code.

{lua:func}`derivation`
: Built-in function to create strings that cause zb to run a {term}`builder program`.

:::

[`pairs`]: https://www.lua.org/manual/5.4/manual.html#pdf-pairs
[`tostring`]: https://www.lua.org/manual/5.4/manual.html#pdf-tostring
[Metatables and Metamethods]: https://www.lua.org/manual/5.4/manual.html#2.4
