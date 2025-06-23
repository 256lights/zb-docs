# zb-specific extensions

This section documents the functions that zb adds to its Lua environment.
All the functions in this section are available as globals.

:::{function} path{path, [name], [filter]}

Copies the file, directory, or symbolic link at `p` into the store.
This is a common way of loading a program's source code into zb.

When `path` is called from a Lua file inside the store directory,
it cannot be called to access files outside the store directory.

:kwparam string path:
  An absolute path or a path relative to the Lua file that called `path`.
  Slash-separated relative paths are accepted on all platforms.

:kwparam string name:
  The name to use for the store object (excluding the digest).
  If omitted, then the last path component of `path` is used as the name.

:kwparam function filter:
  If `filter` is given and `path` names a directory,
  then `path` calls `filter` for each file, directory, or symlink inside the directory.
  The first argument to the `filter` function is a slash-separated path
  relative to the top of the directory of the file currently being filtered.
  The second argument to the `filter` function
  is one of `"regular"`, `"directory"`, or `"symlink"`
  to indicate the type of the file.
  If the filter function returns `nil` or `false`,
  then the file will be excluded from import into the store.
  The default behavior of `path` is equivalent to passing `filter = function() return true end`.

:returns: The absolute path to the imported store object.

:rtype: string

:::

:::{function} path(p)
:noindex:

As a convenience, if you only need to call {lua:func}`path` with the `path` field,
you can pass the string as the sole argument to `path`.

:param string p:
  An absolute path or a path relative to the Lua file that called `path`.
  Slash-separated relative paths are accepted on all platforms.

:returns: The absolute path to the imported store object.

:rtype: string

:::

:::{function} readFile(p)

```{versionadded} 0.2
```

`readFile` reads the contents of a file into a string.

:param string p:
  An absolute path or a path relative to the Lua file that called `readFile`.
  Slash-separated relative paths are accepted on all platforms.

:returns: The content of the file.

:rtype: string

:::

:::{function} derivation(env)

`derivation` adds a [`.drv` file][Derivation Specification] to the store
specifying a {term}`derivation` that can be built.
`derivation` takes a table as its sole argument.
All fields in the table are passed to the {term}`builder program` as environment variables.
The values can be strings, numbers, booleans, or lists of any of the previous types.
A string is used as-is.
Numbers are converted to strings.
`false` is converted to the empty string; `true` is converted to the string `1`.
Each item in a list is converted to a string and then joined with a single space.

The returned derivation object will have a copy of all the fields of the table passed into the `derivation` function that produced it,
plus a few extra fields:

- `drvPath`: a string containing the absolute path
  to the resulting [`.drv` file][Derivation Specification] in the store.
- `out`: a placeholder string that represents the absolute path to the derivation's output.
  Passing this string (or strings formed from it) into other calls to `derivation`
  will implicitly add a build dependency between the derivations.
  (See ["Dependency Information"](deps.md) for details.)

For convenience, using a derivation object in places that expect a string
(e.g. concatenation or a call to `tostring`)
will be treated the same as accessing the `out` field.

The environment that the builder runs in is documented in the [Derivation Specification][].

:kwparam string name:
  The name to use for the derivation
  and the resulting store object (excluding the digest and the `.drv` extension).

:kwparam string system:
  The triple that the derivation can run on.

:kwparam string builder:
  The path to the program to run.

:kwparam string[] args:
  The arguments to pass to the {term}`builder program`.

:kwparam string outputHash:
  If given, the derivation is a fixed-output derivation.
  This argument is a [hash string](hash-string.md) for the derivation's output,
  with its exact meaning determined by `outputHashMode` (see below).
  Derivations with the same `name`, `outputHash`, and `outputHashMode` are considered interchangable,
  regardless of the other fields in the derivation.

:kwparam string outputHashMode:
  This field must not be set unless `outputHash` is also set.
  The value of the field must be one of `flat` (the default) or `recursive`.
  If the value of the field is `flat` or not set,
  then the builder must produce a single file and its contents,
  when hashed with the algorithm given by `outputHash`,
  must produce the same hash as `outputHash`.
  If the value of the field is `recursive`,
  then the builder's output,
  when serialized as a NAR file and hashed with the algorithm given by `outputHash`,
  must produce the same hash as `outputHash`.

:rtype: derivation

:::

[Derivation Specification]: ../derivations.md

:::{function} fetchurl{url, hash, [name], [executable]}

`fetchurl` returns a derivation that downloads a URL.
`fetchurl` takes a table as its sole argument
with the following fields:

:kwparam string url: The URL to download.

:kwparam string hash: A [hash string](hash-string.md) of the file's content.

:kwparam string name:
  The name to use for the store object (excluding the digest).
  If omitted, then the last path component of the `url` is used as the name.

:kwparam boolean executable:
  Whether the file should be marked as executable.
  If true, then the NAR serialization is used to compute the `hash` instead of the file content.

:rtype: derivation

:::

:::{function} extract{src, [name], [stripFirstComponent]}

Returns a derivation that extracts an archive file.

The source must be in one of the following formats:

- .tar
- .tar.gz
- .tar.bz2
- .zip

The algorithm used to extract the archive is selected based on the first few bytes of the file.

:kwparam string src: Path to the file.

:kwparam string name:
  The name to use for the resulting store object (excluding the digest).
  If omitted, then the last path component of the `src` without the file extension is used as the name.

:kwparam boolean stripFirstComponent:
  If `true` or omitted, then the root directory is stripped during extraction.

:rtype: derivation

:::

:::{function} fetchArchive{url, hash, [name], [stripFirstComponent]}

Returns a derivation that extracts an archive from a URL.
This is a convenience wrapper around `fetchurl` and `extract`.

:kwparam string url: The URL to download.

:kwparam string hash:
  The [hash string](hash-string.md) of the archive's content (not the extracted store object).

:kwparam string name:
  The name to use for the store object (excluding the digest).
  If omitted, then the last path component of the `url` is used as the name.

:kwparam boolean stripFirstComponent:
  If `true` or omitted, then the root directory is stripped during extraction.

:rtype: derivation

:::

:::{function} import(path)

Reads the Lua file at the given path and executes it asynchronously.
Every Lua file that zb encounters is treated as a separate module.
This is similar to the `dofile` and `require` functions in standalone Lua
(which are not supported in zb),
but `import` is special in a few ways:

- `import` will load the module for any given path at most once during a run of `zb`.
- `import` does not execute the module right away.
  Instead, `import` returns a placeholder object that acts like the module.
  When you do anything with the placeholder object other than pass it around,
  it will then wait for the module to finish initialization.
  `await` can be used to access the value.
- Globals are not shared among modules.
  Setting a "global" variable in a zb module will place it in a table
  which is implicitly returned by `import`
  if the module does not return any values.
- Everything in a module will be "frozen" when the end of the file is reached.
  This means that any changes to variables or tables (even locals)
  will raise an error.
- If `path` is a path constructed from a derivation,
  then zb will build the derivation before attempting to read it.

When `import` is called from a Lua file inside the store directory,
it cannot be called to access files outside the store directory.

:param string path:
  An absolute path or a path relative to the Lua file that called `path`.
  Slash-separated relative paths are accepted on all platforms.

:returns: A placeholder object for the module.

:rtype: module

:::

:::{function} await(x)

Forces a module (as returned by `import`) to load and returns its value.
If the argument is not a module, then the argument is returned as-is.

:::

:::{function} toFile(name, s)

Creates a non-executable file in the store.

:param string name: File name (excluding digest)

:param string s: File content

:returns: Absolute path to the store file

:rtype: string

:::

:::{function} storePath(path)

Adds a dependency on an existing store path.
If the store object named by `path` does not exist in the store,
`storePath` raises an error.

`storePath` is used to reference store objects that are created outside the zb build
and imported into the store.
Most users should avoid this function, as it is mostly intended for bootstrapping.

:param string path: Absolute {term}`store path`.

:returns:
  A string that is equivalent to its argument
  but includes the dependency information necessary
  for it to be correctly interpreted as a store path.
  (See [dependency information](deps.md) for details.)

:rtype: string

:::

:::{lua:data} storeDir

`storeDir` is a string constant with the running evaluator's {term}`store directory`
(e.g. `/opt/zb/store` or `C:\zb\store`).

:::
