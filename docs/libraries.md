# External Libraries

## Overview

Due to the real time nature of ANC, performance is a signficant consideration for Diminish. It was determing through the build that the Python equivalent libraries for filtering and networking sockets were not fast enough. The decision was made to build out these performance critical pieces in C libraries and leveraging [ctypes](https://docs.python.org/3/library/ctypes.html) to perform the necessary work.

## Build

There are build tasks available via [tasks.py](../tasks.py) and `invoke`. Additionally there are VSCode commands under the Build options to execute the `invoke` commands and ultimately the `gcc` compliation. This compliation step is required on both the client and server.

The compliation step builds shared objects (.so files) and Python through ctypes loads and executes the shared object code.

## Networking Protocol

The networking protocol within these libraries are extremely basic currently. It is expected that a matrix of double values will be sent based on the `STEP_SIZE` environment variable. No additional header or packet information is currently transferred.