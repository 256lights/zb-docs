# Installation Instructions

To install zb:

1. Go to the [latest zb release](https://github.com/256lights/zb/releases/latest)
   in your web browser.
2. Download the binary archive asset for your platform.
3. Extract the binary archive.
   For tarballs, you can run `tar -jxf ${ARCHIVE?}`,
   where `${ARCHIVE?}` is the name of the file you downloaded.
4. On macOS, you may need to run `xattr -r -d com.apple.quarantine ${DIR?}`
   (where `${DIR?}` is the extracted directory)
   to stop Gatekeeper from blocking the installer.
5. On Unix-like systems, run `sudo ./install` inside the extracted directory.
   There is no installer for Windows yet.
   ([#82](https://github.com/256lights/zb/issues/82) tracks adding a Windows installer.)
6. Run `zb version` to verify that your installation worked.
7. You can delete the archive and the extracted directory:
   they are not needed after the installation.

On `aarch64-apple-macos`, the zb standard library requires additional setup.
See the [standard library README](https://github.com/256lights/zb-stdlib/blob/main/README.md) for details.

## What the installer does

The installer does the following in order:

1. Copy {term}`store objects <store object>`
   from the installer directory to the default {term}`store directory`.

2. Create a symbolic link from `/usr/local/bin/zb` to the store object containing zb.

3. Create the `zbld` Unix group and a number of Unix users in the group.

4. On Linux, the installer creates systemd units at `/etc/systemd/system/zb-serve.service`
   and `/etc/systemd/system/zb-serve.socket`.

   On macOS, the installer creates a launchd daemon at `/Library/LaunchDaemons/dev.zb-build.serve.plist`.

The installer is designed to be idempotent:
each step that the installer detects has already installed will be skipped.
This allows you to run the installer to upgrade, downgrade, or repair zb.

The [administrator's guide](admin/index.md) has more details
about how to manage the build server.

## Uninstalling

To fully remove zb from your machine:

1. Stop the systemd units or the launchd daemon.
2. Remove the `/usr/local/bin/zb` symbolic link.
3. Delete the {term}`store directory`.
4. Remove the `zbld` Unix users.
5. Remove the `zbld` Unix group.
