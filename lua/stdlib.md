# Standard Libraries

zb provides the following standard libraries from Lua:

- The [basic functions][] (globals and as `_G`)
- The [math library][] (`math`)
- The [string manipulation library][] (`string`)
- The [table manipulation library][] (`table`)
- The [UTF-8 library][] (`utf8`)
- The [operating system library][] (`os`), albeit in a very limited capacity

Each of these libraries are available as globals and do not require importing.
Unless otherwise noted, the behavior of every symbol in this section
is as documented in the [Lua 5.4 manual][].

[Lua 5.4 manual]: https://www.lua.org/manual/5.4/
[basic functions]: https://www.lua.org/manual/5.4/manual.html#6.1
[math library]: https://www.lua.org/manual/5.4/manual.html#6.7
[operating system library]: https://www.lua.org/manual/5.4/manual.html#6.9
[string manipulation library]: https://www.lua.org/manual/5.4/manual.html#6.4
[table manipulation library]: https://www.lua.org/manual/5.4/manual.html#6.6
[UTF-8 library]: https://www.lua.org/manual/5.4/manual.html#6.5

## Basics (`_G`)

```{module} _G
```

The following [basic functions][] are available as globals:

- [`assert`](https://www.lua.org/manual/5.4/manual.html#pdf-assert)
- [`error`](https://www.lua.org/manual/5.4/manual.html#pdf-error)
- [`getmetatable`](https://www.lua.org/manual/5.4/manual.html#pdf-getmetatable)
- [`ipairs`](https://www.lua.org/manual/5.4/manual.html#pdf-ipairs)
- [`load`](https://www.lua.org/manual/5.4/manual.html#pdf-load)
- [`next`](https://www.lua.org/manual/5.4/manual.html#pdf-next)
- [`pairs`](https://www.lua.org/manual/5.4/manual.html#pdf-pairs)
- [`pcall`](https://www.lua.org/manual/5.4/manual.html#pdf-pcall)
- [`rawequal`](https://www.lua.org/manual/5.4/manual.html#pdf-rawequal)
- [`rawget`](https://www.lua.org/manual/5.4/manual.html#pdf-rawget)
- [`rawlen`](https://www.lua.org/manual/5.4/manual.html#pdf-rawlen)
- [`rawset`](https://www.lua.org/manual/5.4/manual.html#pdf-rawset)
- [`select`](https://www.lua.org/manual/5.4/manual.html#pdf-select)
- [`setmetatable`](https://www.lua.org/manual/5.4/manual.html#pdf-setmetatable)
- [`tonumber`](https://www.lua.org/manual/5.4/manual.html#pdf-tonumber)
- [`tostring`](https://www.lua.org/manual/5.4/manual.html#pdf-tostring)
- [`type`](https://www.lua.org/manual/5.4/manual.html#pdf-type)
- [`warn`](https://www.lua.org/manual/5.4/manual.html#pdf-warn)
- [`xpcall`](https://www.lua.org/manual/5.4/manual.html#pdf-xpcall)

The following variables are available as globals:

- [`_G`](https://www.lua.org/manual/5.4/manual.html#pdf-_G)
- [`_VERSION`](https://www.lua.org/manual/5.4/manual.html#pdf-_VERSION)

Intentionally absent are:

- [`collectgarbage`](https://www.lua.org/manual/5.4/manual.html#pdf-collectgarbage)
- [`dofile`](https://www.lua.org/manual/5.4/manual.html#pdf-dofile)
- [`loadfile`](https://www.lua.org/manual/5.4/manual.html#pdf-loadfile)

[`print`](https://www.lua.org/manual/5.4/manual.html#pdf-print)
is currently missing, but [planned](https://github.com/256lights/zb/issues/40).

## Mathematics

```{module} math
```

The following symbols are available in the [`math` library][math library]:

- [`abs`](https://www.lua.org/manual/5.4/manual.html#pdf-math.abs)
- [`acos`](https://www.lua.org/manual/5.4/manual.html#pdf-math.acos)
- [`asin`](https://www.lua.org/manual/5.4/manual.html#pdf-math.asin)
- [`atan`](https://www.lua.org/manual/5.4/manual.html#pdf-math.atan)
- [`ceil`](https://www.lua.org/manual/5.4/manual.html#pdf-math.ceil)
- [`cos`](https://www.lua.org/manual/5.4/manual.html#pdf-math.cos)
- [`deg`](https://www.lua.org/manual/5.4/manual.html#pdf-math.deg)
- [`exp`](https://www.lua.org/manual/5.4/manual.html#pdf-math.exp)
- [`tointeger`](https://www.lua.org/manual/5.4/manual.html#pdf-math.tointeger)
- [`floor`](https://www.lua.org/manual/5.4/manual.html#pdf-math.floor)
- [`fmod`](https://www.lua.org/manual/5.4/manual.html#pdf-math.fmod)
- [`ult`](https://www.lua.org/manual/5.4/manual.html#pdf-math.ult)
- [`log`](https://www.lua.org/manual/5.4/manual.html#pdf-math.log)
- [`max`](https://www.lua.org/manual/5.4/manual.html#pdf-math.max)
- [`min`](https://www.lua.org/manual/5.4/manual.html#pdf-math.min)
- [`modf`](https://www.lua.org/manual/5.4/manual.html#pdf-math.modf)
- [`rad`](https://www.lua.org/manual/5.4/manual.html#pdf-math.rad)
- [`sin`](https://www.lua.org/manual/5.4/manual.html#pdf-math.sin)
- [`sqrt`](https://www.lua.org/manual/5.4/manual.html#pdf-math.sqrt)
- [`tan`](https://www.lua.org/manual/5.4/manual.html#pdf-math.tan)
- [`type`](https://www.lua.org/manual/5.4/manual.html#pdf-math.type)
- [`pi`](https://www.lua.org/manual/5.4/manual.html#pdf-math.pi)
- [`huge`](https://www.lua.org/manual/5.4/manual.html#pdf-math.huge)
- [`maxinteger`](https://www.lua.org/manual/5.4/manual.html#pdf-math.maxinteger)
- [`mininteger`](https://www.lua.org/manual/5.4/manual.html#pdf-math.mininteger)

Intentionally absent are:

- [`random`](https://www.lua.org/manual/5.4/manual.html#pdf-math.random)
- [`randomseed`](https://www.lua.org/manual/5.4/manual.html#pdf-math.randomseed)

## String Manipulation

```{module} string
```

The following symbols are available in the [`string` library][string manipulation library]:

- [`byte`](https://www.lua.org/manual/5.4/manual.html#pdf-string.byte)
- [`char`](https://www.lua.org/manual/5.4/manual.html#pdf-string.char)
- [`find`](https://www.lua.org/manual/5.4/manual.html#pdf-string.find)
- [`format`](https://www.lua.org/manual/5.4/manual.html#pdf-string.format)
- [`gmatch`](https://www.lua.org/manual/5.4/manual.html#pdf-string.gmatch)
- [`gsub`](https://www.lua.org/manual/5.4/manual.html#pdf-string.gsub)
- [`len`](https://www.lua.org/manual/5.4/manual.html#pdf-string.len)
- [`lower`](https://www.lua.org/manual/5.4/manual.html#pdf-string.lower)
- [`match`](https://www.lua.org/manual/5.4/manual.html#pdf-string.match)
- [`pack`](https://www.lua.org/manual/5.4/manual.html#pdf-string.pack)
- [`packsize`](https://www.lua.org/manual/5.4/manual.html#pdf-string.packsize)
- [`rep`](https://www.lua.org/manual/5.4/manual.html#pdf-string.rep)
- [`reverse`](https://www.lua.org/manual/5.4/manual.html#pdf-string.reverse)
- [`sub`](https://www.lua.org/manual/5.4/manual.html#pdf-string.sub)
- [`upper`](https://www.lua.org/manual/5.4/manual.html#pdf-string.upper)

Intentionally absent is:

- [`dump`](https://www.lua.org/manual/5.4/manual.html#pdf-string.dump)

[`string.unpack`](https://www.lua.org/manual/5.4/manual.html#pdf-string.unpack)
is currently missing but [planned](https://github.com/256lights/zb/issues/79).

zb also sets a metatable for strings where the `__index` field points to the `string` table.

### Patterns

[Patterns][] behave a little differently in zb's implementation
in order to avoid pathological runtime performance and clean up some confusing behaviors.
Patterns do not support backreferences (i.e. `%0` - `%9`) or balances (i.e. `%b`).
Attempting to use either of these pattern items will raise an error.
In patterns, character sets with classes in ranges (e.g. `[%a-z]`)
raise an error instead of silently exhibiting undefined behavior.
However, ranges using escapes (e.g. ``[%]-`]``) are well-defined in this implementation.

[Patterns]: https://www.lua.org/manual/5.4/manual.html#6.4.1

## Table Manipulation

```{module} table
```

All of the symbols in the [`table` library][table manipulation library] are available:

- [`concat`](https://www.lua.org/manual/5.4/manual.html#pdf-table.concat)
- [`insert`](https://www.lua.org/manual/5.4/manual.html#pdf-table.insert)
- [`move`](https://www.lua.org/manual/5.4/manual.html#pdf-table.move)
- [`pack`](https://www.lua.org/manual/5.4/manual.html#pdf-table.pack)
- [`remove`](https://www.lua.org/manual/5.4/manual.html#pdf-table.remove)
- [`sort`](https://www.lua.org/manual/5.4/manual.html#pdf-table.sort)
- [`unpack`](https://www.lua.org/manual/5.4/manual.html#pdf-table.unpack)

## UTF-8

```{module} utf8
```

All of the symbols in the [`utf8` library][UTF-8 library] are available:

- [`char`](https://www.lua.org/manual/5.4/manual.html#pdf-utf8.char)
- [`charpattern`](https://www.lua.org/manual/5.4/manual.html#pdf-utf8.charpattern)
- [`codepoint`](https://www.lua.org/manual/5.4/manual.html#pdf-utf8.codepoint)
- [`codes`](https://www.lua.org/manual/5.4/manual.html#pdf-utf8.codes)
- [`len`](https://www.lua.org/manual/5.4/manual.html#pdf-utf8.len)
- [`offset`](https://www.lua.org/manual/5.4/manual.html#pdf-utf8.offset)

## Operating System

```{module} os
```

The only symbol available in the [`os` library][operating system library]
is [`os.getenv`](https://www.lua.org/manual/5.4/manual.html#pdf-os.getenv).

```{function} os.getenv(varname)

Returns the value of the process environment variable `varname`
or `fail` if the variable is not defined
or not in the allow-list of variables permitted by the user.

:param string varname: Environment variable name.

:rtype: string|nil
```
