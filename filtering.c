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

  return_signal->data = malloc (len * n * sizeof(double));
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
  for (int i = 0; i < signal->length; i++) {
    for (int j = 0; j < signal->n; j++) {
      signal->data[j+i*signal->n] = data[j+i*signal->n];
    }
  }
}

error_t extract(signal* input, int k, signal* result) {
  error_t error = E_SUCCESS;
  if(k >= input->length) {
    error = E_OUT_OF_BOUNDS;
    return error;
  }

  for (int i = 0; i < input->n; i++) {
    result->data[i] = input->data[k*input->n+i];
  }

  return error;
}

void print_signal(signal* signal) {
  printf("==================\n");
  for (int i = 0; i < signal->length; i++) {
    printf("sample "); 
    printf(ANSI_COLOR_BLUE "%d" ANSI_COLOR_RESET ": [", i);
    for (int j = 0; j < signal->n; j++) {
      if(j < signal->n - 1) {
        printf(ANSI_COLOR_MAGENTA "%f" ANSI_COLOR_RESET ",", signal->data[j+i*signal->n]);
      }
      else {
        printf(ANSI_COLOR_MAGENTA "%f" ANSI_COLOR_RESET "", signal->data[j+i*signal->n]);
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
      adotb->data[i*b->n+j] = product;
    }
  }

  return error;
}

error_t subtract(signal* a, signal* b, signal* asubb) {
  error_t error = E_SUCCESS;
  if(a->n != b->n || a->length != b->length) {
    error = E_INVALID_MATRIX_DIMENSIONS;
    return error;
  }

  for (int i = 0; i < a->length; i++) {
    for (int j = 0; j < a->n; j++) {
      asubb->data[j+i*a->n] = a->data[j+i*a->n] - b->data[j+i*a->n];
    }
  }

  return error;
}

error_t add(signal* a, signal* b, signal* aplusb) {
  error_t error = E_SUCCESS;
  if(a->n != b->n || a->length != b->length) {
    error = E_INVALID_MATRIX_DIMENSIONS;
    return error;
  }

  for (int i = 0; i < a->length; i++) {
    for (int j = 0; j < a->n; j++) {
      aplusb->data[j+i*a->n] = a->data[j+i*a->n] + b->data[j+i*a->n];
    }
  }

  return error;
}

error_t multiply(signal* signal, double multiplier) {
  error_t error = E_SUCCESS;
  for(int i = 0; i < signal->n*signal->length; i++) {
    signal->data[i] = signal->data[i] * multiplier;
  }
  return error;
}

error_t divide(signal* signal, double divisor) {
  error_t error = E_SUCCESS;
  for(int i = 0; i < signal->n*signal->length; i++) {
    signal->data[i] = signal->data[i] / divisor;
  }
  return error;
}

error_t transpose(signal* input, signal* transposed) {
  error_t error = E_SUCCESS;

  for (int i = 0; i < input->length; i++) {
    for (int j = 0; j < input->n; j++) {
      transposed->data[i+j*transposed->n] = input->data[j+i*input->n];
    }
  }

  return error;
}

/*
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
}*/

void lms(double *target_signal_in, double *input_signal_in, double mu, int n, double *y_out, double *e_out, int length) {
  signal* target_signal = initialize_signal(n, length);
  unmarshall(target_signal, target_signal_in);

  signal* input_signal = initialize_signal(n, length);
  unmarshall(input_signal, input_signal_in);

  signal* weights = initialize_signal(n, 1);
  zeros(weights);

  for (int k = 0; k < length; k++) {
    signal* kth_input = initialize_signal(n, 1);
    zeros(kth_input);
    signal* result = initialize_signal(1, 1);
    zeros(result);

    extract(input_signal, k, kth_input);
    dot(weights, kth_input, result);
    y_out[k] = result->data[0];
    e_out[k] = target_signal->data[k] - y_out[k];

    multiply(kth_input, mu * e_out[k]);
    add(weights, kth_input, weights);

    destroy_signal(kth_input);
    destroy_signal(result);
  }

  destroy_signal(target_signal);
  destroy_signal(input_signal);
  destroy_signal(weights);
}
