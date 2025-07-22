# Glossary

:::{glossary}

builder program
  The program run in a {term}`derivation`.
  Sometimes shortened to "builder".

derivation
  A build step.
  A description of a program to run — called a {term}`builder program` —
  to produce files.
  Derivations can depend on the results of other derivations.
  Derivations are created with the {lua:func}`derivation` built-in function.
  See the [Derivation Specification](derivations.md) for a full reference.

store directory
  A collection of build artifacts and source files,
  each of which is called a {term}`store object`.

  The conventional store directory is:

  - `/opt/zb/store` on Linux and macOS
  - `C:\zb\store` on Windows

store object
  A file, directory, or symbolic link that is an immediate child of the {term}`store directory`.

store path
  An absolute filesystem path of a {term}`store object`.
  See the page on [Store Paths](paths.md) for a full reference.

system value
system triple
  The `system` value of a {term}`derivation` is used to specify a class of machines that can execute the derivation's {term}`builder <builder program>`.
  The format is intentionally compatible with [LLVM target triples][]
  (which are, in turn, similar to GCC target triples).
  `system` values are a hyphen-separated collection of architecture, vendor, operating system, and environment components.
  Common values include:

  - `x86_64-unknown-linux` for Linux running on a 64-bit Intel CPU
  - `aarch64-apple-macos` for macOS running on a 64-bit ARM processor (Apple Silicon)
  - `x86_64-pc-windows` for Windows running on a 64-bit Intel CPU

  The full syntax of a `system` value is defined in [`system` values specification][].

:::

[LLVM target triples]: https://clang.llvm.org/docs/CrossCompilation.html#target-triple
[`system` values specification]: https://github.com/256lights/zb/blob/main/internal/system/README.md
