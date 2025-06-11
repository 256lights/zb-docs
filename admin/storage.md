# Storage

```{eval-rst}
.. index:: store directory
```

As mentioned in [Architecture](architecture.md), a store server manages a single {term}`store directory`.
Along with the build artifacts themselves,
zb must maintain metadata about the build artifacts and their relationships.
If this metadata is lost, zb is unable to use the store artifacts.
Such metadata is stored in a [SQLite][] database.
The exact schema of this database and its contents is considered internal
and may change from release to release.

zb also stores build logs alongside its database.
These logs are periodically deleted to reclaim space.
The exact layout of this directory is considered internal
and may change from release to release,
but generally, it will contain plain text files with the combined stdout and stderr
of builders run.

[SQLite]: https://www.sqlite.org/

## `zb serve` Options

```{program} zb serve
```

:::{option} --db <path>

The path to the metadata database.
The default path is:

- `/opt/zb/var/zb/db.sqlite` on Linux and macOS
- `C:\zb\var\zb\db.sqlite` on Windows

:::

:::{option} --log-directory <path>

The directory to write build logs to.
The default directory is:

- `/opt/zb/var/log/zb` on Linux and macOS
- `C:\zb\var\log\zb` on Windows

:::

:::{option} --build-log-retention <duration>

Time before build logs are aged out.
Default is `168h` (7 days).

:::
