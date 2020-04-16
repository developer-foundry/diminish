# soundwave

## Install

```
pip3 install -r requirements.txt
pip3 install invoke
```

## Running

```
python3 -m soundwave -a nlms -f data/truck-and-construction-noises.wav -t data/pink-noise.wav
```

If you wish to use the fast LMS C library you must run the `build c` task or the following commands before running the python library (to ensure the C shared library is compiled on your machine)

```
invoke build
```

or

```
gcc -c -Wall -Werror -fpic clms.c
gcc -shared -o libclms.so clms.o
```

The algorithms available (-a cli parameter) are `lms`, `nlms`, `nsslms`, `rls`, and `clms` (fast lms using C library)

## Bluetooth 

Running bluetooth in compatibility mode,

by modifying `/etc/systemd/system/dbus-org.bluez.service,`

changing

`ExecStart=/usr/lib/bluetooth/bluetoothd`

into

`ExecStart=/usr/lib/bluetooth/bluetoothd -C`

You will get a permission denied error.

Need to perform the following steps:

```
$ cat /etc/group | grep bluetooth
bluetooth:x:113:pi
$ sudo usermod -G bluetooth -a pi
$ sudo chgrp bluetooth /var/run/sdp
```

Then perform a `sudo vim` on `/etc/systemd/system/var-run-sdp.path` and add the following contents:

```
[Unit]
Descrption=Monitor /var/run/sdp

[Install]
WantedBy=bluetooth.service

[Path]
PathExists=/var/run/sdp
Unit=var-run-sdp.service
```

Then perform a `sudo vim` on `/etc/systemd/system/var-run-sdp.service` and add the following contents:

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



## Tests

```
python3 -m pytest tests
```
