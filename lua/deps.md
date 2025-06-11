```{eval-rst}
.. index:: string; dependencies
```

# Dependency Information in Strings

Lua strings in zb that represent a store path carry extra dependency information
that is used when creating store objects derived from those strings.
For example, passing a string returned from the `path` function
into the `derivation` function will add the store path as an input to the derivation.
Similarly, passing the `out` field of a derivation object to another `derivation` function call
will add the derivation object as a build dependency of the new derivation.

String dependency information is not directly accessible in the Lua environment,
but its effects are observable.
The standard Lua functions and operators that manipulate strings are aware of such dependency information
and will preserve them where possible.
Examples of this include:

- Using the `..` operator to concatenate two strings
  will include the dependency information of both operands.
- The string returned by `string.format` will include dependency information
  from its arguments.
- Substrings from `string.match` or `string.sub` will include dependency information
  from the input string, if applicable.

The notable exception is if a string is serialized and deserialized in some way
(e.g. with `string.byte`), the dependency information will be stripped.
This is not a common thing to do in most build configurations,
but doing so can cause the dependency graph to be incorrect.
