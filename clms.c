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

int length = 0;
int n = 0;
float eps = 0.1;
float mu = 0.0;
float weights[2]; //TODO refactor to support variable

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

void zeroes(float *signal, int length) {
  for(int i = 0; i < length; i++) {
    signal[i] = 0.0;
  }
}

float dot(float *weights, float *input) {
  return weights[0] * input[0] + weights[1] * input[1];
}

float * sub(struct Signal *input, int index) {
  float * diff = malloc (sizeof(float) * 2);
  diff[0] = input->channel_one[index];
  diff[1] = input->channel_two[index];
  return diff;
}

float subone(struct Signal *input, int index) {
  return input->channel_one[index];
}

float * multi(float mulptilicand, float * input) {
  float * result = malloc (sizeof(float) * 2);
  result[0] = input[0] * mulptilicand;
  result[1] = input[1] * mulptilicand;
  return result;
}

void add(float * weights, float * dw) {
  weights[0] = weights[0] + dw[0];
  weights[1] = weights[1] + dw[1];
}

/*y = np.zeros(N)
e = np.zeros(N)
self.w_history = np.zeros((N, self.n))
# adaptation loop
for k in range(N):
    self.w_history[k,:] = self.w
    y[k] = np.dot(self.w, x[k])
    e[k] = d[k] - y[k]
    R1 = np.dot(np.dot(np.dot(self.R,x[k]),x[k].T),self.R)
    R2 = self.mu + np.dot(np.dot(x[k],self.R),x[k].T)
    self.R = 1/self.mu * (self.R - R1/R2)
    dw = np.dot(self.R, x[k].T) * e[k]
    self.w += dw*/
void rls(float *targetSignalIn, float *inputSignalIn, float muParam, int nParam, float *y, float *e, int lengthParam) {
  length = lengthParam;
  mu = muParam;
  n = nParam;

  struct Signal *targetSignal = newSignal(length);
  unmarshallTarget(targetSignal, targetSignalIn, length); //TODO refactor to not be specific to target or input

  struct Signal *inputSignal = newSignal(length);
  unmarshallInput(inputSignal, inputSignalIn, length);

  zeroes(y, length);
  zeroes(e, length);
  zeroes(weights, 2); //TODO might need to change to random instead

  for (int k = 0; k < length; k++) {
    y[k] = dot(weights, sub(inputSignal, k));
    e[k] = subone(targetSignal,k) - y[k];
    float * dw = multi(mu * e[k], sub(inputSignal,k));
    add(weights,dw);
  }

  delSignal(targetSignal);
  delSignal(inputSignal);
}

void lms(float *targetSignalIn, float *inputSignalIn, float muParam, int nParam, float *y, float *e, int lengthParam) {
  length = lengthParam;
  mu = muParam;
  n = nParam;

  struct Signal *targetSignal = newSignal(length);
  unmarshallTarget(targetSignal, targetSignalIn, length); //TODO refactor to not be specific to target or input

  struct Signal *inputSignal = newSignal(length);
  unmarshallInput(inputSignal, inputSignalIn, length);

  zeroes(y, length);
  zeroes(e, length);
  zeroes(weights, 2); //TODO might need to change to random instead

  for (int k = 0; k < length; k++) {
    y[k] = dot(weights, sub(inputSignal, k));
    e[k] = subone(targetSignal,k) - y[k];
    float * dw = multi(mu * e[k], sub(inputSignal,k));
    add(weights,dw);
  }

  delSignal(targetSignal);
  delSignal(inputSignal);
}
