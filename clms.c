#include <stdio.h>
#include <stdlib.h>

//TODO need to change this to support variable number of columns
//right now it is hardcoded to support two - the combination of
//input and target passed in from python
struct Signal {
  float *channel_one;
  float *channel_two;
  float *channel_one_start;
  float *channel_two_start;
  int length;
};

struct Signal *newSignal (size_t sz) {
  struct Signal *retSignal = malloc (sizeof(struct Signal));
  if (retSignal == NULL) {
    return NULL;
  }
  retSignal->channel_one = malloc (sz * sizeof(float*));
  if (retSignal->channel_one == NULL) {
    free(retSignal);
    return NULL;
  }

  retSignal->channel_two = malloc (sz * sizeof(float*));
  if (retSignal->channel_two == NULL) {
    if (retSignal->channel_one != NULL) free(retSignal->channel_one);
    free(retSignal);
    return NULL;
  }

  retSignal->length = sz;
  retSignal->channel_one_start = retSignal->channel_one;
  retSignal->channel_two_start = retSignal->channel_two;
  return retSignal;
}

void delSignal (struct Signal *signal) {
  if (signal != NULL) {
    free(signal->channel_one);
    free(signal->channel_two);
    free(signal);
  }
}

void unmarshallTarget(struct Signal *signal, float *arr, int length) {
  for(int i = 0; i < length; i++) {
    *(signal->channel_one) = *arr;
    if (i == 0) {
      signal->channel_one_start = signal->channel_one;
    }
    signal->channel_one++;
    arr++;
  }
  signal->channel_one = signal->channel_one_start;
}

void unmarshallInput(struct Signal *signal, float *arr, int length) {
  for(int i = 0; i < length*2; i++) {
    if (i % 2 == 0) {
      *(signal->channel_one) = *arr;
      if (i == 0) {
        signal->channel_one_start = signal->channel_one;
      }
      signal->channel_one++;
    }
    else {
      *(signal->channel_two) = *arr;
      if (i == 1) {
        signal->channel_two_start = signal->channel_two;
      }
      signal->channel_two++;
    }
    arr++;
  }
  signal->channel_one = signal->channel_one_start;
  signal->channel_two = signal->channel_two_start;
}

void print_signal(struct Signal *signal) {
  float *channel_one; 
  float *channel_two;
  channel_one = signal->channel_one_start;
  channel_two = signal->channel_two_start;

  for (int i = 0; i < signal->length; i++) {
    printf("Sample %d: [%f, %f]\n", i, *channel_one, *channel_two);
    channel_one++;
    channel_two++;
  }
}

void copy(float *signal, float *target, int length) {
  for(int i = 0; i < length; i++) {
    signal[i] = target[i];
  }
}

void lms(float *targetSignalIn, float *inputSignalIn, float mu, int n, float *y, float *e, int length) {
  struct Signal *targetSignal = newSignal(length);
  unmarshallTarget(targetSignal, targetSignalIn, length);

  struct Signal *inputSignal = newSignal(length);
  unmarshallInput(inputSignal, inputSignalIn, length);

  copy(y, targetSignalIn, length);
  copy(e, inputSignalIn, length*2);

  delSignal(targetSignal);
  delSignal(inputSignal);
}
