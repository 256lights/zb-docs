The value of the `__outputs` [metatable](https://www.lua.org/manual/5.4/manual.html#2.4) field can be:

- A function.
  The function will be called with the original table
  and the current {term}`system triple` as its two arguments.
- A value with an `__outputs` field in its metatable.
  The field will be processed recursively
  (up to an implementation-defined limit).
- Any non-`nil` value,
  which will be used instead of the original table.
