# zb documentation

zb
(pronounced "zee bee" or "zeeb")
is an experiment in hermetic, reproducible build systems.
It has not stabilized and should not be used for production purposes.

If you're new to zb, check out the [Getting Started guide](getting-started.md).

## What is zb?

zb is a tool for reproducibly building software, similar to [Bazel][].
(See the [comparison page](project:#bazel-comparison) if you're curious to know the differences.)
When a software build process is [reproducible][@wikipedia_reproducible_2025],
it will produce the exact same output
when given the same inputs.
Reproducibility is a desirable property for a software build process to have:
it simplifies debugging,
it enables build speed-ups,
and it is essential for [digital supply chain security][].
However, reproducibility is a difficult goal to achieve.

Many software build processes are not reproducible
because they neglect to ensure the same versions of their development tools or libraries (dependencies)
are used across machines.
Approaches like virtual machines or containers lock dependency versions across machines,
but rely on large base binary images
that themselves can't be reproduced or audited.
Anyone who has built a Dockerfile containing an `apt-get install` command
has likely been bitten by a package changing versions on them
and causing their software to break.
Virtual machines and containers also make common development tasks harder:
attaching debuggers,
integrating with IDEs,
or even inspecting files can be a chore.
Presented with such great friction,
many developers (understandably) give up on reproducibility.
They use other approaches to use dependencies during development that are "close enough"
to what's running in production.
"Close enough" is frequently not enough, and complexity ensues.

zb simplifies reproducible builds.

- zb lets users define their build process using [Lua][].
  Lua has been [used in a variety of applications][@wikipedia_lua_2024]
  to provide scripting facilities.
- zb runs every build step in a lightweight sandbox
  with limited environment variables and filesystem access
  to reduce the likelihood of unexpected dependencies.
  The sandbox doesn't rely on containers or virtual machines,
  so zb works even in restricted continuous integration (CI) environments.
- zb stores build artifacts as plain files and directories.
  so you can run development tools and build artifacts
  directly from zb's store.
  This means you can point your IDE to use the exact compiler or intepreter
  that your build is using, for example.
  It also means that zb's build artifacts can be copied directly into a container or virtual machine image
  without fuss.
- zb stores all build artifacts and source code in [content-addressable storage][].
  The name of a build directory includes a [hash][] of all its contents,
  so it's easy to see at a glance whether two versions of a dependency are the same.
- Consistency of build artifact paths across machines
  enables distributed caching and remote builds.

[@wikipedia_reproducible_2025]: https://en.wikipedia.org/wiki/Reproducible_builds
[@wikipedia_lua_2024]: https://en.wikipedia.org/wiki/Lua_(programming_language)#Applications
[Bazel]: https://bazel.build/
[content-addressable storage]: https://en.wikipedia.org/wiki/Content-addressable_storage
[digital supply chain security]: https://en.wikipedia.org/wiki/Digital_supply_chain_security
[hash]: https://en.wikipedia.org/wiki/Cryptographic_hash_function
[Lua]: https://www.lua.org/

```{toctree}
:maxdepth: 2
:hidden:

Installation <install>
getting-started
admin/index
comparison
```

```{toctree}
:caption: Reference
:hidden:

Language Reference <lua/index>
derivations
binary-cache/index
paths
glossary
genindex
```

```{toctree}
:caption: Community
:hidden:

support
Contributing <CONTRIBUTING>
```
