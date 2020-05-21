# Diminish

## Overview

Diminish is an implementation of active noise cancellation. It is not generic purpose at this stage though that may eventually be a part of the [Roadmap](https://diminish.ai/#/). Right now it is intended as a reference architecture and proof of concept. Please see the [documentation](https://diminish.ai/#/) for more details.

## Table of Contents
- [Background](#background)
- [Features](#features)
- [Setup](#setup)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Environment Variables](#environment-variables)
- [Usage](#usage)
    - [Server](#server)
    - [Client](#client)
- [Documentation](#documentation)
- [License](#license)
- [Contributing](#contributing)
- [Authors](#authors)

## Background
There are commercial applications that are being considered, but currently this is proof of concept work to experiment with various real world scenarios. See [Roadmap](https://diminish.ai/#/) for future considerations.

## Features

- Active Noise Cancellation with Error Microphone, Reference Microphone, Output Speaker
- Reference Microphone over TCP/IP
- Support for multiple algorithms though [Recursive Least Squares](https://en.wikipedia.org/wiki/Recursive_least_squares_filter) is the only one currently implemented
- External C libraries for filtering algorithm and networking - this was necessary to get near real time performance
- Terminal User Interface for server role
- Client User Interface for server and client
- Plotting signals using [Matplotlib](https://matplotlib.org/) to enable analysis and debugging


## Setup

### Prerequisites
- Python3
- Pip3
- Ubuntu 19 which includes the correct version of [PulseAudio](https://www.freedesktop.org/wiki/Software/PulseAudio/). Note version 20 has a higher version that will not work correctly with Diminish.
- gcc compiler
- npm
- docsify(https://docsify.js.org/#/)

### Installation
```
git clone git@github.com:developer-foundry/diminish.git
sudo apt update
sudo apt install build-essential
npm i docsify-cli -g
pip3 install -r requirements.txt
cp environment/.env.example environment/.env
```

### Environment Variables

* `MODE` - options are `prerecorded` or `live`. `prerecorded` performs the active noise cancellation setup on a set of configured files. See `INPUT_FILE` and `TARGET_FILE`.
* `ALGORITHM` - `crls` is current the only option and is the algorithm that works the fastest and converges the fastest. See [documentation](https://diminish.ai/#/) for additional details.
* `INPUT_FILE` - only needed in `prerecorded` mode. Defines the input signal. Has only been tested with `.wav` files.
* `TARGET_FILE` - required for all modes of operation. The target signal that the application will converge towards. Samples include `data/silence.wav` and `data/pink-noise.wav`. Has only been tested with `.wav` files.
* `DEVICE` - the hardware device id. Can be modified, but to use your default output and input use `DEVICE=default`.
* `SIZE` - only needed in `prerecorded` mode. Allows user to control the amount of data processed by the algorithm.
* `ROLE` - specifies is the process is running as `SERVER` or as `CLIENT`. `SERVER` is the primary processing unit and also assumes the speaker and error microphone are attached. `CLIENT` is a secondary device and assumes the reference microphone is attached.
* `WAIT_SIZE` - specifices an initialze number of data frames the buffers should hold before processing. A good default value is 5000.
* `STEP_SIZE` - specifies the number of data frames the algorithm should process in a given run. A good default value is 1024.
* `LOGLEVEL` - specifies the verbosity of logs generated. The default is `INFO`.
* `SERVER` - specifies the IP address (IPv4) of the server. If running as the `SERVER` role, this can just be set to `127.0.01`.
* `PORT` - specifies the port number the client should connect to the server on. The default should be set to `65432`.

## Usage

Diminish assumes that a client and a server role are running. See [documentation](https://diminish.ai/#/) for additional details and reference diagrams. The directions below specify the command line tasks to run, but for VSCode users there is also a `tasks.json` that provides access to these commands via Build tasks.

?> Note it is important that `invoke build-libraries` is run on both the client and server before the python process is called. This generates the necessary C libraries that are required to execute. See [documentation](https://diminish.ai/#/) for additional details.

### Server

The server can be run using either the terminal user interface (TUI) or the command line interface (CLI). The TUI is useful for running and monitoring and the CLI is useful for debugging.

#### Example `.env`
```
MODE=live
ALGORITHM=crls
INPUT_FILE=data/truck-and-construction-noises.wav
TARGET_FILE=data/pink-noise.wav
DEVICE=default
SIZE=300000
ROLE=server
WAIT_SIZE=5000
STEP_SIZE=1024
LOGLEVEL=INFO
SERVER=127.0.0.1
PORT=65432
```

#### TUI

Useful for monitoring the application over time. The TUI specifies keybindings that can be seen on screen to start, pause and quit processing.
```
python3 -m tui
```

<div class="sequence">
    <img src="./assets/tuirecording.svg"/>
</div>

#### CLI

Useful for debugging or experimentation
```
python3 -m cli
```

### Client

The client can only be run using the command line interface (CLI).

#### Example `.env`
```
MODE=live
ALGORITHM=crls
INPUT_FILE=data/truck-and-construction-noises.wav
TARGET_FILE=data/pink-noise.wav
DEVICE=default
SIZE=300000
ROLE=client
WAIT_SIZE=5000
STEP_SIZE=1024
LOGLEVEL=INFO
SERVER=192.168.193.224
PORT=65432
```

#### CLI

Useful for debugging or experimentation. The client does support pausing the algorithm using the `p` keybinding.
```
python3 -m cli
```

## Documentation

See the `docs` folder or navigate to [documentation](https://diminish.ai/#/). Documentation is generated via [docsify](https://docsify.js.org/#/) and any terminal videos were generated via [svg-term-cli](https://github.com/marionebl/svg-term-cli)

## License

See [License](LICENSE)

## Contributing

Right now diminish is not accepting contributions, but please check back in the future

## Authors

- Keith LaForce ([klaforce](https://github.com/klaforce/))
- Eric LaForce ([elaforc](https://github.com/elaforc/))