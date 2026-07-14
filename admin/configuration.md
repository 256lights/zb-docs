```{eval-rst}
.. index:: ! single: server; configuration value
```

# Server Configuration

The following are server-specific [configuration settings](../configuration.md).
They are placed in a top-level `"server"` key, like this:

```json
// config.jwcc
{
  "server": {
    // ... server properties here ...
  }
}
```

:::{confval} server.download
:type: object
:default: `null`

The `server.download` setting is a [store locator](project:#store-locator)
that specifies a store that the server will download
{term}`store objects <store object>` and {term}`realizations <realization>` from
when the server receives a request to realize a {term}`derivation` output it does not have in its local store
before attempting to run its {term}`builder program`.

:::

:::{confval} server.upload
:type: object
:default: `null`

The `server.upload` setting is a [store locator](project:#store-locator)
that specifies a store that the server will upload
{term}`store objects <store object>` and {term}`realizations <realization>` to
after the server successfully runs a {term}`builder program`.

:::
