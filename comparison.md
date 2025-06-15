# Comparison with other tools

This document aims to highlight the differences between zb and other tools.

(bazel)=
## Bazel

Bazel and zb share the very similar goal to build software in a reproducible manner.
zb mostly differs in how it achieves the goal:

- Bazel requires reworking the build graph to be written in terms of [Bazel rules][].
  This typically requires surrounding tooling (IDEs, etc.) to be Bazel-aware.
  Setting up a zb build process is less involved
  because it leverages existing build tooling appropriate for each ecosystem.
  You can easily run `zb derivation env` on any build step
  to obtain a `.env` file to emulate the build environment.
- zb uses Lua instead of [Starlark][], Bazel's bespoke Python-like language.
  zb uses Lua to leverage existing learning resources for Lua.
- Bazel has different APIs for [creating rules][Bazel rules API] and [macros][Bazel macros].
  zb does not draw such a distinction:
  all build steps invoke a single program.
  zb functions can be written to automate creation of build steps.
- zb build artifacts have a consistent file path across hosts
  and can have dependencies on other build artifacts.
  This eliminates the need for [runfiles][]
  and makes dynamic linking simpler.

[Bazel rules]: https://bazel.build/rules
[Bazel rules API]: https://bazel.build/extending/rules
[Bazel macros]: https://bazel.build/extending/macros
[runfiles]: https://bazel.build/reference/be/common-definitions#common.data
[Starlark]: https://bazel.build/rules/language

(nix)=
## Nix

Many of the techniques in zb were pioneered by the [Nix][] package manager.
zb is built on the principles in the [original paper by Eelco Dolstra][@dolstra_purely_2006],
but differs in some key ways:

- zb is focused on building software, not managing packages.
  We don't anticipate a large, central package repository for zb
  nor a Linux distribution.
  There's a lot of overlap in dependency management,
  but the audience and affordances differ in subtle ways.
- zb deliberately focuses on broad usability.
  For example, zb supports Windows
  and uses Lua instead of a domain-specific language.
- zb uses content-addressed derivations.
  This is a long-standing [experimental feature in Nix][ca-derivations],
  whereas zb does not even support Nix's default "input-addressed" mode.
  This was chosen to simplify the architecture,
  enable build optimizations,
  and prevent build artifact corruption.

[ca-derivations]: https://nix.dev/manual/nix/2.24/development/experimental-features.html#xp-feature-ca-derivations
[@dolstra_purely_2006]: https://edolstra.github.io/pubs/phd-thesis.pdf
[Nix]: https://nixos.org/
