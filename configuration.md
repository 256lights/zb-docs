# Configuration Reference

When running the zb command-line interface,
zb will gather configuration data from files in the local filesystem.
Command-line flags or environment variables will override any settings in the configuration files.

## Format

zb reads its configuration in [JSON With Commas and Comments][JWCC] format.
This is a strict superset of JSON that permits:

- trailing commas in arrays and objects
- C++ style `/* block comments */` and `// line comments`

[JWCC]: https://nigeltao.github.io/blog/2021/json-with-commas-comments.html

## Location

### Linux and macOS

On Linux and macOS systems, zb follows the [XDG Base Directory Specification][]
to find its configuration files.
The files used are (in decreasing order of precedence):

1. `$XDG_CONFIG_HOME/zb/config.jwcc`.
   If `$XDG_CONFIG_HOME` is not set, it defaults to `$HOME/.config`.
2. `$XDG_CONFIG_HOME/zb/config.json`.
   If `$XDG_CONFIG_HOME` is not set, it defaults to `$HOME/.config`.
3. For each directory in `$XDG_CONFIG_DIRS` separated by colons
   (defaulting to `/etc/xdg`):
    a. `zb/config.jwcc` underneath the directory
    b. `zb/config.json` underneath the directory

[XDG Base Directory Specification]: https://specifications.freedesktop.org/basedir/0.8/

### Windows

On Windows systems, zb will find configuration files at (in decreasing order of precedence):

1. `%AppData%\zb\config.jwcc`
2. `%AppData%\zb\config.json`

## Properties

:::{confval} debug

Whether to include logging useful for debugging zb itself.
This is generally very verbose and should only be enabled if you are reporting an issue with zb.
Equivalent to the `--debug` command-line flag.

:::

:::{confval} storeDirectory

Absolute path to the store directory.

Defaults to:

- `/opt/zb/store` on Linux and macOS
- `C:\zb\store` on Windows

Will be overridden by {envvar}`ZB_STORE_DIR`.

:::

:::{confval} storeSocket

Absolute path of the store server Unix socket to use or,
in the case of `zb serve`, to create.
The default is:

- `/opt/zb/var/zb/server.sock` on Linux and macOS
- `C:\zb\var\zb\server.sock` on Windows

Will be overridden by {envvar}`ZB_STORE_SOCKET`.

:::

:::{confval} cacheDB

Absolute path to a SQLite database that contains cache data for speeding up zb.
This database can be deleted at any time: it exists purely to speed up builds.
The default is:

- `$XDG_CACHE_HOME/zb/cache.db` on Linux and macOS.
  `$XDG_CACHE_HOME` defaults to `$HOME/.cache`.
- `%LocalAppData%\zb\cache.db` on Windows

Equivalent to the `--cache` command-line flag.

:::

:::{confval} allowEnvironment

The `allowEnvironment` setting configures the behavior of {lua:func}`os.getenv`.

- If `true`, then {lua:func}`os.getenv` can retrieve any environment variable
  in the zb process's environment.
  Equivalent to passing `--allow-all-env` on the command line.
- If `false`, then {lua:func}`os.getenv` will always return `nil`.
- If the setting is an array,
  then it is interpreted as a set of environment variable names
  that {lua:func}`os.getenv` will retrieve from the zb process's environment.
  {lua:func}`os.getenv` will return `nil`
  for any environment variable whose name is not in the array.
  Equivalent to passing `--allow-env` with each name on the command line.

`allowEnvironment` settings are not merged:
the setting from the file with the highest precedence will be used.

:::

:::{confval} trustedPublicKeys

The `trustedPublicKeys` setting is an array of public keys that zb will trust for existing build results
when building a {term}`derivation`.
`trustedPublicKeys` settings are merged across all configuration files.
Each public key is a JSON object with the following fields:

| Field       | Type   | Description                               |
| :---------- | :----- | :---------------------------------------- |
| `format`    | string | Only `"ed25519"` is defined at the moment |
| `publicKey` | string | Base64-encoded public key data            |

For more details on the content of these fields,
see [realization signature specification](project:#realization-signatures).

If the configuration files do not include any trusted public keys,
then any previous build result can be reused
unless the `--clean` command-line option is passed.

:::
