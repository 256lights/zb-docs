```{eval-rst}
.. index:: graphical user interface, web interface
```

# Graphical User Interface

A zb server can optionally run a web server that provides a graphical user interface (GUI).
This GUI allows viewing the status of running builds and inspection of the store.
Administrators can enable the GUI by passing a flag like `--ui=localhost:8080` to `zb serve`.
Once the server has started, the user can view the GUI by visiting `http://localhost:8080`
in a web browser on the same machine as `zb serve`.

## `zb serve` options

```{program} zb serve
```

:::{option} --ui [host]:port

If specified, then serve the GUI over HTTP on the given TCP port.
If a `host` is specified, then the HTTP port will only be available on the interface with the given address.

:::

:::{option} --allow-remote-ui

For security reasons, connections are only permitted from the local machine by default,
even if the address given to the `zb serve --ui` flag specifies an external interface.
The `zb serve --allow-remote-ui` disables this protection.

:::
