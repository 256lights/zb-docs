# Language Differences

zb's Lua language semantics differ from Lua 5.4 in two key ways:

- [Weak tables][] (i.e. the `__mode` metafield) are not supported.
- The [`__gc` (finalizer) metamethod][Garbage-Collection Metamethods]
  is never called by zb's runtime.
  Finalizers are not guaranteed to run in Lua,
  so this is technically within specification,
  but this document calls it out so readers are aware.

Aside from this, all other aspects of the language should be the same.
Refer to the [Lua 5.4 manual][] for details.

[Lua 5.4 manual]: https://www.lua.org/manual/5.4/
[Garbage-Collection Metamethods]: https://www.lua.org/manual/5.4/manual.html#2.5.3
[Weak tables]: https://www.lua.org/manual/5.4/manual.html#2.5.4
