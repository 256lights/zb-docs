# zb documentation

zb
(pronounced "zee bee" or "zeeb")
is an experiment in hermetic, reproducible build systems.
It has not stabilized and should not be used for production purposes.

If you're new to zb, check out the [Getting Started guide](getting-started.md).

[Lua]: https://www.lua.org/
[Nix]: https://nixos.org/
[dolstra_purely_2006]: https://edolstra.github.io/pubs/phd-thesis.pdf
[mokhov_build_2018]: https://doi.org/10.1145/3236774

## Why zb?

zb is based on the ideas in [The purely functional software deployment model by Eelco Dolstra][dolstra_purely_2006]
and [Build systems à la carte][mokhov_build_2018],
as well as the author's experience in working with build systems.
The build model is mostly the same as in [Nix][],
but build targets are configured in [Lua][]
instead of a domain-specific language.

For more motivation on the development of zb,
see the early blog posts:

- [zb: A Build System Prototype](https://www.zombiezen.com/blog/2024/06/zb-build-system-prototype/)
- [zb: An Early-Stage Build System](https://www.zombiezen.com/blog/2024/09/zb-early-stage-build-system/)

## Hello World

```lua
hello = derivation {
  name    = "hello";
  infile  = path "hello.txt";
  builder = "/bin/sh";
  system  = "x86_64-linux";
  args    = {"-c", "while read line; do echo \"$line\"; done < $infile > $out"};
}
```

```{toctree}
:maxdepth: 2
:hidden:

Installation <install>
getting-started
admin/index
```

```{toctree}
:caption: Reference
:hidden:

Language Reference <lua/index>
derivations
glossary
genindex
```
