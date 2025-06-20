# Getting Started

This introductory guide will help you run your first build with zb
and explain the basic concepts you will need to use zb.
zb is a build system that manages your dependencies
so that you can be confident that a build that works on one machine
works on any machine with the same operating system and CPU architecture.

## Prerequisites

This guide assumes:

- Familiarity with the command-line interface for your operating system.
  (For example, Terminal.app on macOS, Command Prompt or PowerShell on Windows, etc.)
- Knowledge of at least one programming language.
  We will be building a C program in this tutorial,
  but you do not need to know C or have any specific version of developer tools installed.
  Installing tools automatically is a key feature of zb!
- zb uses the [Lua programming language](https://www.lua.org/) to configure builds.
  Learning Lua is helpful for using zb.
  zb uses the Lua 5.4 language,
  with some standard libraries omitted to limit the complexity of builds.
  As such, any learning resources for Lua will be applicable to zb.

The standard library currently supports:

- `x86_64-unknown-linux`
- `aarch64-apple-macos`

## Installation

If you haven't already, follow the [installation instructions](install.md).

## First Steps

Let's start with a C "Hello, World" program.
Open your editor of choice and enter the following into a new file `hello.c`:

```{literalinclude} tutorial/hello.c
:language: c
```

Now let's learn how to build `hello.c` into an executable with zb.

We will write a small Lua script that describes the build,
and then use the zb command-line interface (CLI) to run the script.

Out of the box, zb only knows how to run programs and download source.
However, zb has a standard library that can be fetched
to provide tools for some common programming languages.
In your editor, enter the following into a new file `zb.lua`
in the same directory as `hello.c`
(we'll walk through this code in a moment):

```{literalinclude} tutorial/zb.lua
:language: lua
:end-before: sqlite3 =
```

Now we can build the program with `zb build`.
Note that the first time you run `zb build`,
will take a while,
since it is building the standard library tools from source.
(Because zb build artifacts can be safely shared among machines,
there are plans to speed this up.
[#43](https://github.com/256lights/zb/issues/43) tracks this work.)

```shell
zb build 'zb.lua#hello'
```

`zb build` takes in a URL of Lua file to run.
The fragment (i.e. everything after the `#`)
names a variable to build.
In this case, we're building `hello`.
`zb build` will automatically look for a global called `hello` defined inside `zb.lua`.

At the end, `zb build` will print the path to the directory it created,
something like `/opt/zb/store/2lvf1cavwkainjz32xzja04hfl5cimx6-hello`.
As you might expect from the `installPhase` we used above,
it will be inside the `bin` directory we created inside the output directory.

```console
% /opt/zb/store/2lvf1cavwkainjz32xzja04hfl5cimx6-hello/bin/hello
Hello, World!
```

In the next few sections, we'll explain the `zb.lua` script in more detail.

### Derivation Basics

The first section downloads [the standard library][] from GitHub:

```{literalinclude} tutorial/zb.lua
:language: lua
:start-after: -- Download the standard library.
:end-before: -- Import modules from the standard library.
```

{lua:func}`fetchArchive` is a built-in global function that returns a {term}`derivation`
that extracts the tarball or zip file downloaded from a URL.

A {term}`derivation` in zb is a build step:
a description of a program — called a {term}`builder <builder program>` — to run to produce files.
Derivations can depend on the results of other derivations.
Creating a derivation does not run its builder;
creating a derivations records how to invoke its builder.
We use `zb build` to run builders,
or as we'll see in a moment,
the {lua:func}`import` function will implicitly run the builder.

Finally, derivations can be used like strings.
For example, derivations can be concatenated or passed as an argument to `tostring`.
Such a string is a placeholder for the derivation's output file or directory,
and when used for other derivations,
it implicitly adds a dependency on the derivation.

[the standard library]: https://github.com/256lights/zb-stdlib

### Modules and Imports

The next section loads a Lua module from the zb standard library:

```{literalinclude} tutorial/zb.lua
:language: lua
:start-after: -- Import modules from the standard library.
:end-before: -- Copy the source to the store.
```

Every Lua file that zb encounters is treated as a separate module.
The {lua:func}`import` built-in global function returns the module at the path given as an argument.
This is similar to the `dofile` and `require` functions in standalone Lua
(which are not supported in zb),
but `import` is special in a few ways:

- `import` will load the module for any given path at most once during a run of `zb`.
- `import` does not execute the module right away.
  Instead, `import` returns a placeholder object that acts like the module.
  When you do anything with the placeholder object other than pass it around,
  it will then wait for the module to finish initialization.
- Globals are not shared among modules.
  Setting a "global" variable in a zb module will place it in a table
  which is implicitly returned by `import`
  if the module does not return any values.
- Everything in a module will be "frozen" when the end of the file is reached.
  This means that any changes to variables or tables (even locals)
  will raise an error.

Together, these aspects allow imports to be reordered or run lazily
without fear of unintended side effects.

One other interesting property of the {lua:func}`import` function
is that if you use a path created from a derivation,
it will build the derivation.
So `zb.."/stdenv/stdenv.lua"` will build the `zb` derivation
and then import the [`stdenv/stdenv.lua` file](https://github.com/256lights/zb-stdlib/blob/v0.1.1/stdenv/stdenv.lua)
inside the output.

### Making the Source Available to the Build

The {lua:func}`path` built-in function imports files for use in a derivation:

```{literalinclude} tutorial/zb.lua
:language: lua
:start-after: -- Copy the source to the store.
:end-before: -- Create our build target.
```

The `filter` function allows us to create an allow-list of files in the folder to use.
Changing any file inside a source causes the derivation to be rebuilt on the next `zb build`,
so minimizing the number of files is important for faster incremental builds.

### Creating a Derivation

Finally, we declare a `hello` variable with a derivation value:

```{literalinclude} tutorial/zb.lua
:language: lua
:start-after: -- Create our build target.
:end-before: sqlite3 =
```

`stdenv.makeDerivation` is a function that returns a derivation.
It provides GCC and a minimal set of standard Unix tools.
If the source contains a Makefile, then it uses that to build.
However, for our simple single-file program, we provide a `buildPhase` directly.
`buildPhase` specifies a snippet of Bash script that builds the program in the source directory.
The `installPhase` specifies a snippet of Bash script
to copy the program to `$out`,
the path to where the derivation's output must be placed.

:::{note}

`\z` is Lua's line continuation escape sequence.
As per the [Lua reference manual](https://www.lua.org/manual/5.4/manual.html#3.1):

> The escape sequence `\z` skips the following span of whitespace characters, including line breaks;
> it is particularly useful to break and indent a long literal string into multiple lines
> without adding the newlines and spaces into the string contents.

:::

## Using Dependencies

Now that we know the basics, let's see how to pull in a C library from the internet.
Add the following to the end of `zb.lua`:

```{literalinclude} tutorial/zb.lua
:language: lua
:start-at: sqlite3 =
:end-before: -- Dependencies:
```

Like before, we can build it with `zb build zb.lua#sqlite3`.
Because the source archive includes a `configure` script and a Makefile,
then `stdenv.makeDerivation` knows how to build the package.
You can see that the resulting directory includes `bin/sqlite3`,
a `lib` directory,
and an `include` directory.

Now let's see how to compile the [SQLite Quickstart](https://www.sqlite.org/quickstart.html) example.
Create another file, `hello_sql.c`, in the same directory as `zb.lua`:

```{literalinclude} tutorial/hello_sql.c
:language: c
```

Then add to the end of `zb.lua`:

```{literalinclude} tutorial/zb.lua
:language: lua
:start-after: -- Dependencies:
```

This is mostly the same as our `hello` example from before,
but we do a few new things:

- We import the [`strings.lua` file](https://github.com/256lights/zb-stdlib/blob/v0.1.1/strings.lua)
  from the standard library.
  The `strings.makeIncludePath` and `strings.makeLibraryPath` functions
  join the elements in the table with colons
  and appends `/include` or `/lib`, respectively, to each element.
- We set the `C_INCLUDE_PATH` and `LIBRARY_PATH` environment variables
  to point to the `sqlite3` derivation.
  As you'll recall, derivations can be used like strings
  and automatically introduce a dependency from `hello_sql` to `sqlite3`.

## Wrapping Up

In this guide, we wrote a simple build configuration for a single-file C program.
Then, we built SQLite from source,
and finally, we built a C program that used SQLite as a dependency.

Throughout this tutorial, there have been links to reference documentation.
The [language reference](lua/index.md) describes the flavor of Lua that zb understands,
as well as its built-in functions.
The [standard library repository](https://github.com/256lights/zb-stdlib)
includes other packages and utility functions that can be useful.

Here are the final versions of the files:

- [zb.lua](tutorial/zb.lua)
- [hello.c](tutorial/hello.c)
- [hello_sql.c](tutorial/hello_sql.c)

zb is still in early development.
If you have questions or feedback, see the [support guide](support.md).
If you're interested in getting involved, see the [contributing guide](CONTRIBUTING.md).
