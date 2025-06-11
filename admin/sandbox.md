```{eval-rst}
.. index:: builder program; sandboxing
```

# Sandboxing and Permissions

On Unix-like systems,
store servers require elevated permissions to create sandboxes
and keep {term}`store objects <store object>` unmodifiable by ordinary users.
However, {term}`builders <builder program>` are run with limited separate privileges
to avoid performing sensitive operations during a build.
Concurrent builds are run with separate UIDs to avoid interference among builders.
The installer automatically creates a group called `zbld`,
and populates it with a few dozen users for this purpose.
The group name created by the installer can be changed via the `./install --build-users-group` flag.

zb supports sandboxing builds on Linux systems
so that builders can only access the inputs declared by the build,
along with some basic system directories.
An allow list of files can be added to the sandbox with the `zb serve --sandbox-path` flag.
On Linux, the installer will automatically include a `/bin/sh`
that references a statically compiled version of [BusyBox][].

[BusyBox]: https://busybox.net/

## `zb serve` options

```{program} zb serve
```

:::{option} --build-users-group <name>

The name of the Unix group containing Unix users that {term}`builders <builder program>` should run as.
The store directory must be writable by members of the group.
When `zb serve` is run as root, it will look for the `zbld` group by default.

:::

:::{option} --sandbox=<0|1>

Whether to enable or disable sandboxing.
If `zb serve` is being run as root on Linux, this behavior is enabled by default.

:::

:::{option} --sandbox-path <path>

Register a path that can be used in the sandbox
if specified in a {term}`derivation`'s `__buildSystemDeps`.

:::

:::{option} --implicit-system-dep <path>

Register a path that will always be present in the sandbox.

:::
