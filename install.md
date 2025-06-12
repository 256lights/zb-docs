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

See the [administrator's guide](admin/index.md) for more details on what the installer does.
