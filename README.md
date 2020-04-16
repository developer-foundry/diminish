# soundwave

## Install

```
pip3 install -r requirements.txt
```

## Environment Variables
Example .env file

```
MODE=anc
ALGORITHM=crls
INPUT_FILE=data/truck-and-construction-noises.wav
TARGET_FILE=data/pink-noise.wav
DEVICE=default
SIZE=300000
BT_MODE=server
```

* `MODE` - options are `prerecorded`, `live`, and `anc`.
* `ALGORITHM` - options are `lms`, `nlms`, `nsslms`, `rls`, `clms`, `crls`. The current algorithm that works the fastest and converges the fastest is `crls`.
* `INPUT_FILE` - only needed in `prerecorded` mode. Defines the input signal. Has only been tested with `.wav` files.
* `TARGET_FILE` - required for all modes of operation. The target signal that the application will converge towards. Samples include `data/silence.wav` and `data/pink-noise.wav`. Has only been tested with `.wav` files.
* `DEVICE` - the hardware device id. Can be modified, but to use your default output and input use `DEVICE=default`.
* `SIZE` - only needed in `prerecorded` mode. Allows user to control the amount of data processed by the algorithm.
* `BT_MODE` - only used in `anc` mode. Options are `client` and `server`. Typicall, you will run in `client` mode on the reference microphone device and `server` mode on the ANC device connected to the error microphone.

## Running

```
python3 -m soundwave
```

If you wish to use the fast C algorithms you must run the `build c` task in VSCode or the following commands before running the python library (to ensure the C shared library is compiled on your machine)

```
invoke build
```

or

```
gcc -c -Wall -Werror -fpic clms.c
gcc -shared -o libclms.so clms.o
```

## Bluetooth Configuration

The bluetooth configuration requires running bluetooth in compatibility mode on the ANC device or the device that is in `server` mode. You can turn this on by performing the following steps on your server device:

1. Edit `/etc/systemd/system/dbus-org.bluez.service`
2. Change `ExecStart=/usr/lib/bluetooth/bluetoothd` to `ExecStart=/usr/lib/bluetooth/bluetoothd -C`
3. Run `python3 -m soundwave`
4. You should get a permission denied error.
5. Need to perform the following steps:
    1. `cat /etc/group | grep bluetooth`
    2. `sudo usermod -G bluetooth -a pi`
    3. `sudo chgrp bluetooth /var/run/sdp`
    4. Then perform a `sudo vim` on `/etc/systemd/system/var-run-sdp.path` and add the following contents:
        ```
        [Unit]
        Descrption=Monitor /var/run/sdp

        [Install]
        WantedBy=bluetooth.service

        [Path]
        PathExists=/var/run/sdp
        Unit=var-run-sdp.service
        ```
    5. Then perform a `sudo vim` on `/etc/systemd/system/var-run-sdp.service` and add the following contents:
        ```
        [Unit]
        Description=Set permission of /var/run/sdp

        [Install]
        RequiredBy=var-run-sdp.path

        [Service]
        Type=simple
        ExecStart=/bin/chgrp bluetooth /var/run/sdp
        ExecStartPost=/bin/chmod 662 /var/run/sdp
        ```
    6. Run the following commands to restart bluetooth dameon
        ```
        sudo systemctl daemon-reload
        sudo systemctl enable var-run-sdp.path
        sudo systemctl enable var-run-sdp.service
        sudo systemctl start var-run-sdp.path
        ```
6. Set the environment variables correctly to run server mode.
7. Run `python3 -m soundwave`

## Tests

```
python3 -m pytest tests
```
