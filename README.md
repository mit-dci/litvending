# litvending

This is a few little scripts to get the Raspberry Pi in that one vending
machine on the third floor of the Media Lab to accept payments over the
Lightning Network.

It uses [Lit](https://github.com/mit-dci/lit), which is an experimental
Lightning node implementation developed by the
[Digtial Currency Initiaive](https://dci.mit.edu/).

## quarterexec

This directory contains the Arduino source code that runs on the Arduino in the
machine.  It was taken from an older project before LN existed, so there's a
few problems with it as-is.  I'm making it cleaner and better some other time.
