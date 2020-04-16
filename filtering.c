#include "filtering.h"

struct signal {
  double* data; /** stores all input data up to number of inputs n */
  size_t n; /** the number of inputs to filter. This is also the number of columns in the matrix */
  size_t length; /** the length of each input. This is also the number of rows in the matrix */
};

char const*const error_message(error_t error) {
  return errordesc[error].message;
}

signal* initialize_signal(size_t n, size_t len) {
  signal* return_signal = malloc (sizeof(signal));

  if (return_signal == NULL) {
    return NULL;
  }

  return_signal->data = malloc (len * n * sizeof return_signal->data);
  if (return_signal->data == NULL) {
    free(return_signal);
    return NULL;
  }

  return_signal->length = len;
  return_signal->n = n;
  return return_signal;
}

void destroy_signal(signal* signal) {
  if (signal != NULL) {
    free(signal->data);
    free(signal);
  }
}

void unmarshall(signal* signal, double* data) {
  for (int i = 0; i < signal->n; i++) {
    for (int j = 0; j < signal->length; j++) {
      signal->data[j+i*signal->length] = data[j+i*signal->length];
    }
  }
}

void print_signal(signal* signal) {
  printf("==================\n");
  for (int i = 0; i < signal->n; i++) {
    printf("sample "); 
    printf(ANSI_COLOR_BLUE "%d" ANSI_COLOR_RESET ": [", i);
    for (int j = 0; j < signal->length; j++) {
      if(j < signal->length - 1) {
        printf(ANSI_COLOR_MAGENTA "%f" ANSI_COLOR_RESET ",", signal->data[j+i*signal->length]);
      }
      else {
        printf(ANSI_COLOR_MAGENTA "%f" ANSI_COLOR_RESET "", signal->data[j+i*signal->length]);
      }
    }
    printf("]\n");
  }
  printf("==================\n");
}

void zeros(signal* signal) {
  for(int i = 0; i < signal->n*signal->length; i++) {
    signal->data[i] = 0.0;
  }
}

error_t dot(signal* a, signal* b, signal* adotb) {
  error_t error = E_SUCCESS;
  if(a->n != b->length) {
    error = E_INVALID_MATRIX_DIMENSIONS;
    return error;
  }

  for(int i = 0; i < a->length; i++) {
    for(int j = 0; j < b->n; j++) {
      double product = 0.F;
      for(int k = 0; k < a->n; k++) {
        product += a->data[k+i*a->n] * b->data[k*b->n+j];
      }
      adotb->data[i*a->length+j] = product;
    }
  }

  return error;
}

/*
//assumes matrixOne is 2x2 and matrixTwo is 1x2
double *dotp(double *matrixOne, double *matrixTwo) {
  double * result = malloc (sizeof(double) * 4);
  result[0] = matrixOne[0] * matrixTwo[0] + matrixOne[1] * matrixTwo[1];
  result[1] = matrixOne[2] * matrixTwo[0] + matrixOne[3] * matrixTwo[1];
  return result;
}

//assumes matrixOne is 1x2 and matrixTwo is 2x2
double *dotpreverse(double *matrixOne, double *matrixTwo) {
  double * result = malloc (sizeof(double) * 4);
  result[0] = matrixOne[0] * matrixTwo[0] + matrixOne[1] * matrixTwo[1];
  result[1] = matrixOne[0] * matrixTwo[2] + matrixOne[1] * matrixTwo[3];
  return result;
}

//assumes matrixOne is 2x1 and matrixTwo is 1x2
double dotdouble(double *matrixOne, double *matrixTwo) {
  double result = 0.0;
  result = matrixOne[0] * matrixTwo[0] + matrixOne[1] * matrixTwo[1];
  return result;
}

//explicit for weights - should be generalized to dotdouble
double dot(double *weights, double *input) {
  return weights[0] * input[0] + weights[1] * input[1];
}

//indexing for Signal struct
double * sub(signal *input, int index) {
  double * diff = malloc (sizeof(double) * 2);
  diff[0] = input->channel_one[index];
  diff[1] = input->channel_two[index];
  return diff;
}

//indexing for Signal struct
double subone(signal *input, int index) {
  return input->channel_one[index];
}

//multiple a matrix by a scalar
double * multi(double mulptilicand, double * input) {
  double * result = malloc (sizeof(double) * 2);
  result[0] = input[0] * mulptilicand;
  result[1] = input[1] * mulptilicand;
  return result;
}

//multiple a matrix by a scalar
double * multifour(double mulptilicand, double * input) {
  double * result = malloc (sizeof(double) * 4);
  result[0] = input[0] * mulptilicand;
  result[1] = input[1] * mulptilicand;
  result[2] = input[2] * mulptilicand;
  result[3] = input[3] * mulptilicand;
  return result;
}

//divide a matrix by a scalar
double * divide(double *matrix, double divisor) {
  double * result = malloc (sizeof(double) * 4);
  result[0] = matrix[0] / divisor;
  result[1] = matrix[1] / divisor;
  result[2] = matrix[2] / divisor;
  result[3] = matrix[3] / divisor;
  return result;
}

//subtract two matricies of equal size
//assumes a 2x2 matrix
double * subtract(double *matrixOne, double *matrixTwo) {
  double * result = malloc (sizeof(double) * 4);
  result[0] = matrixOne[0] - matrixTwo[0];
  result[1] = matrixOne[1] - matrixTwo[1];
  result[2] = matrixOne[2] - matrixTwo[2];
  result[3] = matrixOne[3] - matrixTwo[3];
  return result;
}

//should be refactored to be more generic
void add(double * weights, double * dw) {
  weights[0] = weights[0] + dw[0];
  weights[1] = weights[1] + dw[1];
}

//transpose a generic size matrix
double * transpose(double * input, int length) {
  double * result = malloc (sizeof(double) * length);
  for (int i = 0; i < length; i++)
    for (int j = 0; j < length; j++)
      result[i*j] = input[j*i];
  return result;
}

void rls(double *targetSignalIn, double *inputSignalIn, double muParam, int nParam, double *y, double *e, int lengthParam) {
  length = lengthParam;
  mu = muParam;
  n = nParam;

  signal *targetSignal = newSignal(length);
  unmarshallTarget(targetSignal, targetSignalIn, length); //TODO refactor to not be specific to target or input

  signal *inputSignal = newSignal(length);
  unmarshallInput(inputSignal, inputSignalIn, length);

  zeroes(y, length);
  zeroes(e, length);
  zeroes(weights, 2);

  double * R = malloc (sizeof(double) * 4);
  double r_eps = 1 / EPS;
  R[0] = 1*r_eps;
  R[1] = 0;
  R[2] = 0;
  R[3] = 1*r_eps;
  for (int k = 0; k < length; k++) {
    y[k] = dot(weights, sub(inputSignal, k));
    e[k] = subone(targetSignal,k) - y[k];

    double *inputTranspose = transpose(sub(inputSignal, k), 2);
    double *dotRInput = dotp(R, sub(inputSignal, k));
    double dotRInputTranspose = dotdouble(dotRInput, inputTranspose);
    double *R1 = multifour(dotRInputTranspose, R);

    double * dotInputR = dotpreverse(sub(inputSignal, k), R);
    double dotInputRTranspose = dotdouble(dotInputR, inputTranspose);
    double R2 = mu + dotInputRTranspose;

    double * r1DivideR2 = divide(R1, R2);
    double * rMinusR1DivideR2 = subtract(R, r1DivideR2);
    R = multifour((1 / mu), rMinusR1DivideR2);

    double * dw = multi(e[k], dotp(R, inputTranspose));
    add(weights,dw);
  }

  delSignal(targetSignal);
  delSignal(inputSignal);
}

void lms(double *targetSignalIn, double *inputSignalIn, double muParam, int nParam, double *y, double *e, int lengthParam) {
  length = lengthParam;
  mu = muParam;
  n = nParam;

  signal *targetSignal = newSignal(length);
  unmarshallTarget(targetSignal, targetSignalIn, length); //TODO refactor to not be specific to target or input

  signal *inputSignal = newSignal(length);
  unmarshallInput(inputSignal, inputSignalIn, length);

  zeroes(y, length);
  zeroes(e, length);
  zeroes(weights, 2); //TODO might need to change to random instead

  for (int k = 0; k < length; k++) {
    y[k] = dot(weights, sub(inputSignal, k));
    e[k] = subone(targetSignal,k) - y[k];
    double * dw = multi(mu * e[k], sub(inputSignal,k));
    add(weights,dw);
  }

  delSignal(targetSignal);
  delSignal(inputSignal);
}*/

int main() {
  int an = 3;
  int alen = 3;
  double* data = malloc (alen * an * sizeof(double));
  for (int i = 0; i < an; i++) {
    for (int j = 0; j < alen; j++) {
      data[j+i*alen] = (double)(j+i*alen);
    }
  }
  signal* a = initialize_signal(an, alen);
  unmarshall(a, data);
  print_signal(a);

  int bn = 3;
  int blen = 3;
  free(data);
  data = malloc (blen * bn * sizeof(double));
  for (int i = 0; i < bn; i++) {
    for (int j = 0; j < blen; j++) {
      data[j+i*blen] = (double)(j+i*blen);
    }
  }
  signal* b = initialize_signal(bn, blen);
  unmarshall(b, data);
  free(data);
  print_signal(b);

  signal* adotb = initialize_signal(alen, bn);
  error_t result = dot(a, b, adotb);
  if(result == E_SUCCESS) {
    print_signal(adotb);
    printf("Success\n");
  }
  else {
    printf("Error %s\n", error_message(result));
  }

  destroy_signal(a);
  destroy_signal(b);
  destroy_signal(adotb);
  return 0;
}