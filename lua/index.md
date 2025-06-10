# Lua as used by zb

zb uses [Lua 5.4][Lua 5.4 manual] to configure builds.
Where possible, zb tries to maintain compatibility with Lua 5.4
so that resources or tooling for Lua can be used with zb.
However, to facilitate the goal of fast and reproducible builds,
zb does make some minor alterations to the standard libraries available.
This document describes the departures from standard Lua
as well as the new built-in globals that control zb's behavior.
This document serves as a specification of zb's Lua:
deviations from this document should be [reported][zb new issue].

```{toctree}
language
stdlib
extensions
deps
hash-string
```

[Lua 5.4 manual]: https://www.lua.org/manual/5.4/
[zb new issue]: https://github.com/256lights/zb/issues/new/choose
