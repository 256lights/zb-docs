# Comparison with Nix

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
