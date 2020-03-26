# soundwave

## Install

```
pip3 install -r requirements.txt
```

## Running

```
python3 -m soundwave -a nlms -f data/truck-and-construction-noises.wav -t data/pink-noise.wav
```

The algorithms available (-a cli parameter) are `lms`, `nlms`, and `nsslms`

## Tests

```
python3 -m pytest tests
```
