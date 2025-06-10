# Architecture

zb uses a client/server architecture for all builds.
When a user runs `zb build` (or similar invocations),
the zb program acts as a client that connects to a store server — the `zb serve` command.
Typically, a machine runs a single store server.
The store server manages a single {term}`store directory`, which contains build artifacts.

The store directory can be overridden with the `ZB_STORE_DIR` environment variable,
but changing this is discouraged.
Build artifacts can only be shared among store servers with the same store directory path
because build artifacts can contain references to other build artifacts.
For example, a program in one build artifact
may depend on a shared library in another build artifact.
A consistent store directory setting is critical for build reuse.

A zb client communicates with the store server using an [RPC protocol][].
By default, it expects a store server running on the local machine on a Unix domain socket.

[RPC protocol]: https://github.com/256lights/zb/blob/main/internal/zbstorerpc/README.md

## Environment

```{envvar} ZB_STORE_DIR

Absolute path to the store directory.

Defaults to:

- `/opt/zb/store` on Linux and macOS
- `C:\zb\store` on Windows
```

```{envvar} ZB_STORE_SOCKET
Path of the store server Unix socket to use or,
in the case of `zb serve`, to create.
The default is:

- `/opt/zb/var/zb/server.sock` on Linux and macOS
- `C:\zb\var\zb\server.sock` on Windows
```
