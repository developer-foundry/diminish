#include <stdio.h>
#include <stdlib.h>

#define ANSI_COLOR_RED     "\x1b[31m"
#define ANSI_COLOR_GREEN   "\x1b[32m"
#define ANSI_COLOR_YELLOW  "\x1b[33m"
#define ANSI_COLOR_BLUE    "\x1b[34m"
#define ANSI_COLOR_MAGENTA "\x1b[35m"
#define ANSI_COLOR_CYAN    "\x1b[36m"
#define ANSI_COLOR_RESET   "\x1b[0m"

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

//create a zero matrix
void zeroes(float *signal, int length) {
  for(int i = 0; i < length; i++) {
    signal[i] = 0.0;
  }
}

//assumes matrixOne is 2x2 and matrixTwo is 1x2
float *dotp(float *matrixOne, float *matrixTwo) {
  float * result = malloc (sizeof(float) * 4);
  result[0] = matrixOne[0] * matrixTwo[0] + matrixOne[1] * matrixTwo[1];
  result[1] = matrixOne[2] * matrixTwo[0] + matrixOne[3] * matrixTwo[1];
  return result;
}

//assumes matrixOne is 1x2 and matrixTwo is 2x2
float *dotpreverse(float *matrixOne, float *matrixTwo) {
  float * result = malloc (sizeof(float) * 4);
  result[0] = matrixOne[0] * matrixTwo[0] + matrixOne[1] * matrixTwo[1];
  result[1] = matrixOne[0] * matrixTwo[2] + matrixOne[1] * matrixTwo[3];
  return result;
}

//assumes matrixOne is 2x1 and matrixTwo is 1x2
float dotfloat(float *matrixOne, float *matrixTwo) {
  float result = 0.0;
  result = matrixOne[0] * matrixTwo[0] + matrixOne[1] * matrixTwo[1];
  return result;
}

//explicit for weights - should be generalized to dotfloat
float dot(float *weights, float *input) {
  return weights[0] * input[0] + weights[1] * input[1];
}

//indexing for Signal struct
float * sub(struct Signal *input, int index) {
  float * diff = malloc (sizeof(float) * 2);
  diff[0] = input->channel_one[index];
  diff[1] = input->channel_two[index];
  return diff;
}

//indexing for Signal struct
float subone(struct Signal *input, int index) {
  return input->channel_one[index];
}

//multiple a matrix by a scalar
float * multi(float mulptilicand, float * input) {
  float * result = malloc (sizeof(float) * 2);
  result[0] = input[0] * mulptilicand;
  result[1] = input[1] * mulptilicand;
  return result;
}

//multiple a matrix by a scalar
float * multifour(float mulptilicand, float * input) {
  float * result = malloc (sizeof(float) * 4);
  result[0] = input[0] * mulptilicand;
  result[1] = input[1] * mulptilicand;
  result[2] = input[2] * mulptilicand;
  result[3] = input[3] * mulptilicand;
  return result;
}

//divide a matrix by a scalar
float * divide(float *matrix, float divisor) {
  float * result = malloc (sizeof(float) * 2);
  result[0] = matrix[0] / divisor;
  result[1] = matrix[1] / divisor;
  result[2] = matrix[2] / divisor;
  result[3] = matrix[3] / divisor;
  return result;
}

//subtract two matricies of equal size
//assumes a 2x2 matrix
float * subtract(float *matrixOne, float *matrixTwo) {
  float * result = malloc (sizeof(float) * 2);
  result[0] = matrixTwo[0] - matrixOne[0];
  result[1] = matrixTwo[1] - matrixOne[1];
  result[2] = matrixTwo[2] - matrixOne[2];
  result[3] = matrixTwo[3] - matrixOne[3];
  return result;
}

//should be refactored to be more generic
void add(float * weights, float * dw) {
  weights[0] = weights[0] + dw[0];
  weights[1] = weights[1] + dw[1];
}

//transpose a generic size matrix
float * transpose(float * input, int length) {
  float * result = malloc (sizeof(float) * length);
  for (int i = 0; i < length; i++)
    for (int j = 0; j < length; j++)
      result[i*j] = input[j*i];
  return result;
}

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

  //TODO
  //1. Implement R
  //2. Implement transpose
  //3. Implement a divide and subtract
  //self.R = 1/self.eps * np.identity(n)
  /*y[k] = np.dot(self.w, x[k])
  e[k] = d[k] - y[k]
  R1 = np.dot(
        np.dot(
          np.dot(self.R,x[k])
          x[k].T)
        self.R)
  R2 = self.mu + np.dot(np.dot(x[k],self.R),x[k].T)
  self.R = 1/self.mu * (self.R - R1/R2)
  dw = np.dot(self.R, x[k].T) * e[k]
  self.w += dw*/
  float * R = malloc (sizeof(float) * 4);
  float r_eps = 1 / eps;
  R[0] = 1*r_eps;
  R[1] = 0;
  R[2] = 0;
  R[3] = 1*r_eps;
  //printf("mu: " ANSI_COLOR_MAGENTA "%f\n" ANSI_COLOR_RESET, mu);
  //printf("eps: " ANSI_COLOR_MAGENTA "%f\n" ANSI_COLOR_RESET, eps);
  //printf("R: [" ANSI_COLOR_MAGENTA "%f, %f" ANSI_COLOR_RESET "], [" ANSI_COLOR_MAGENTA "%f, %f" ANSI_COLOR_RESET "]\n" , R[0], R[1], R[2], R[3]);
  for (int k = 0; k < length; k++) {
    //float * blah = sub(inputSignal, k);
    //printf("inputSignal[" ANSI_COLOR_BLUE "%d" ANSI_COLOR_RESET "]: [" ANSI_COLOR_MAGENTA "%f, %f" ANSI_COLOR_RESET "]\n", k, blah[0], blah[1]);
    y[k] = dot(weights, sub(inputSignal, k));
    //printf("y[" ANSI_COLOR_BLUE "%d" ANSI_COLOR_RESET "] = " ANSI_COLOR_MAGENTA "%f\n" ANSI_COLOR_RESET, k, y[k]);
    e[k] = subone(targetSignal,k) - y[k];
    //printf("e[" ANSI_COLOR_BLUE "%d" ANSI_COLOR_RESET "] = " ANSI_COLOR_MAGENTA "%f\n" ANSI_COLOR_RESET, k, e[k]);

    float *inputTranspose = transpose(sub(inputSignal, k), 2);
    ////printf("inputTranspose: [" ANSI_COLOR_MAGENTA "%f, %f" ANSI_COLOR_RESET "]\n", inputTranspose[0], inputTranspose[1]);
    float *dotRInput = dotp(R, sub(inputSignal, k));
    //printf("dotRInput: [" ANSI_COLOR_MAGENTA "%f, %f" ANSI_COLOR_RESET "]\n", dotRInput[0], dotRInput[1]);
    float dotRInputTranspose = dotfloat(dotRInput, inputTranspose);
    //printf("dotRInputTranspose: " ANSI_COLOR_MAGENTA "%f\n" ANSI_COLOR_RESET, dotRInputTranspose);
    float *R1 = multifour(dotRInputTranspose, R);
    //printf("R1: [" ANSI_COLOR_MAGENTA "%f, %f" ANSI_COLOR_RESET "], [" ANSI_COLOR_MAGENTA "%f, %f" ANSI_COLOR_RESET "]\n" , R1[0], R1[1], R1[2], R1[3]);

    float * dotInputR = dotpreverse(sub(inputSignal, k), R);
    //printf("dotInputR: [" ANSI_COLOR_MAGENTA "%f, %f" ANSI_COLOR_RESET "]\n", dotInputR[0], dotInputR[1]);
    float dotInputRTranspose = dotfloat(dotInputR, inputTranspose);
    //printf("dotInputRTranspose: " ANSI_COLOR_MAGENTA "%f\n" ANSI_COLOR_RESET, dotInputRTranspose);
    float R2 = mu + dotInputRTranspose;
    //printf("R2: " ANSI_COLOR_MAGENTA "%f\n" ANSI_COLOR_RESET, R2);

    float * r1DivideR2 = divide(R1, R2);
    //printf("R1 Divided by R2: [" ANSI_COLOR_MAGENTA "%f, %f" ANSI_COLOR_RESET "], [" ANSI_COLOR_MAGENTA "%f, %f" ANSI_COLOR_RESET "]\n", r1DivideR2[0], r1DivideR2[1], r1DivideR2[2], r1DivideR2[3]);
    float * rMinusR1DivideR2 = subtract(R, r1DivideR2);
    //printf("R minus R1/R2: [" ANSI_COLOR_MAGENTA "%f, %f" ANSI_COLOR_RESET "], [" ANSI_COLOR_MAGENTA "%f, %f" ANSI_COLOR_RESET "]\n", rMinusR1DivideR2[0], rMinusR1DivideR2[1], rMinusR1DivideR2[2], rMinusR1DivideR2[3]);
    R = multifour((1 / mu), rMinusR1DivideR2);

    float * dw = multi(e[k], dotp(R, inputTranspose));
    //printf("dw: [" ANSI_COLOR_MAGENTA "%f, %f" ANSI_COLOR_RESET "]\n", dw[0], dw[1]);
    add(weights,dw);
    //printf("weights: [" ANSI_COLOR_MAGENTA "%f, %f" ANSI_COLOR_RESET "]\n", weights[0], weights[1]);
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
