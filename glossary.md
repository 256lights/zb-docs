# Glossary

:::{glossary}

builder
builder program
  The program run in a {term}`derivation`.

derivation
  A build step.
  A description of a program to run — called a {term}`builder` —
  to produce files.
  Derivations can depend on the results of other derivations.

store
store directory
  A collection of build artifacts and source files,
  each of which is called a {term}`store object`.

store object
  A file, directory, or symbolic link that is an immediate child of the {term}`store directory`.

store path
  An absolute filesystem path of a {term}`store object`.

system value
system triple
  The `system` value of a {term}`derivation` is used to specify a class of machines that can execute the derivation's {term}`builder`.
  The format is intentionally compatible with [LLVM target triples][]
  (which are, in turn, similar to GCC target triples).
  `system` values are a hyphen-separated collection of architecture, vendor, operating system, and environment components.
  The syntax of a `system` value is defined in [`system` values specification][].
  Example values include:

  - `x86_64-unknown-linux`
  - `aarch64-apple-macos`
  - `x86_64-pc-windows`

:::

[LLVM target triples]: https://clang.llvm.org/docs/CrossCompilation.html#target-triple
[`system` values specification]: https://github.com/256lights/zb/blob/main/internal/system/README.md
