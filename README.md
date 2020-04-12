# soundwave

## Install

```
pip3 install -r requirements.txt
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

## Tests

```
python3 -m pytest tests
```
