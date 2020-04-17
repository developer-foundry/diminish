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

void rls(double *target_signal_in, double *input_signal_in, double mu, int n, double *y_out, double *e_out, int length) {
  signal* target_signal = initialize_signal(n, length);
  unmarshall(target_signal, target_signal_in);

  signal* input_signal = initialize_signal(n, length);
  unmarshall(input_signal, input_signal_in);

  signal* weights = initialize_signal(1, n);
  zeros(weights);

  signal* R = initialize_signal(n, n);
  zeros(R);
  double r_eps = 1 / EPS;
  for(int i = 0; i < n; i++) {
    R->data[i*(R->n+1)] = r_eps;
  }

  for (int k = 0; k < length; k++) {
    /* Initialize temporary variables to ensure memory is properly allocated and freed */
    signal* kth_input = initialize_signal(n, 1);
    zeros(kth_input);
    signal* result = initialize_signal(1, 1);
    zeros(result);
    signal* kth_input_transposed = initialize_signal(kth_input->length, kth_input->n);
    zeros(kth_input_transposed);
    signal* r_dot_kth_input = initialize_signal(kth_input->n,1);
    zeros(r_dot_kth_input);
    signal* r_dot_kth_input_dot_kth_transposed = initialize_signal(1,1);
    zeros(r_dot_kth_input_dot_kth_transposed);
    signal* kth_input_dot_r = initialize_signal(kth_input->n,1);
    zeros(kth_input_dot_r);
    signal* kth_input_dot_r_dot_kth_transposed = initialize_signal(1,1);
    zeros(kth_input_dot_r_dot_kth_transposed);
    signal* r_one_minus_divided = initialize_signal(R->n,R->n);
    zeros(r_one_minus_divided);

    /* Initialize R1 with R as it will become the basis of a multiplication */
    signal* R1 = initialize_signal(R->n,R->n);
    zeros(R1);
    unmarshall(R1, R->data);

    extract(input_signal, k, kth_input);
    dot(kth_input, weights, result);
    y_out[k] = result->data[0];
    e_out[k] = target_signal->data[k] - y_out[k];

    /* Compute R1 (Matrix NxN) */
    transpose(kth_input, kth_input_transposed);
    dot(kth_input, R, r_dot_kth_input);
    dot(r_dot_kth_input, kth_input_transposed, r_dot_kth_input_dot_kth_transposed);
    multiply(R1, r_dot_kth_input_dot_kth_transposed->data[0]);


    /* Computer R2 (Scalar) */
    dot(kth_input, R, kth_input_dot_r);
    dot(kth_input_dot_r, kth_input_transposed, kth_input_dot_r_dot_kth_transposed);
    double R2 = mu + kth_input_dot_r_dot_kth_transposed->data[0];

    /* Compute latest iteration of R */
    divide(R1, R2);
    subtract(R, R1, r_one_minus_divided);
    unmarshall(R, r_one_minus_divided->data);
    multiply(R, (1 / mu));

    /* Compute next set of weights */
    signal* r_one_dot_kth_input_transposed = initialize_signal(1, R->n);
    signal* dw = initialize_signal(weights->n, weights->length);
    zeros(r_one_dot_kth_input_transposed);
    unmarshall(dw, weights->data);
    dot(R, kth_input_transposed, r_one_dot_kth_input_transposed);
    multiply(r_one_dot_kth_input_transposed, e_out[k]);
    add(dw, r_one_dot_kth_input_transposed, weights);

    /* Free memory for next iteration */
    destroy_signal(dw);
    destroy_signal(r_one_dot_kth_input_transposed);
    destroy_signal(kth_input);
    destroy_signal(result);
    destroy_signal(kth_input_transposed);
    destroy_signal(r_dot_kth_input);
    destroy_signal(r_dot_kth_input_dot_kth_transposed);
    destroy_signal(kth_input_dot_r);
    destroy_signal(kth_input_dot_r_dot_kth_transposed);
    destroy_signal(R1);
    destroy_signal(r_one_minus_divided);
  }

  destroy_signal(R);
  destroy_signal(target_signal);
  destroy_signal(input_signal);
  destroy_signal(weights);
}

void lms(double *target_signal_in, double *input_signal_in, double mu, int n, double *y_out, double *e_out, int length) {
  signal* target_signal = initialize_signal(n, length);
  unmarshall(target_signal, target_signal_in);

  signal* input_signal = initialize_signal(n, length);
  unmarshall(input_signal, input_signal_in);

  signal* weights = initialize_signal(1, n);
  zeros(weights);
  /* If you use zero for LMS, it never converges */
  weights->data[0] = (double)rand()/RAND_MAX*1.5-1.0;
  weights->data[1] = (double)rand()/RAND_MAX*1.5-1.0;

  for (int k = 0; k < length; k++) {
    signal* kth_input = initialize_signal(n, 1);
    zeros(kth_input);
    signal* result = initialize_signal(1, 1);
    zeros(result);
    signal* dw = initialize_signal(weights->n, weights->length);
    unmarshall(dw, weights->data);
    signal* kth_input_transposed = initialize_signal(kth_input->length, kth_input->n);
    zeros(kth_input_transposed);

    extract(input_signal, k, kth_input);
    dot(kth_input, weights, result);
    y_out[k] = result->data[0];
    e_out[k] = target_signal->data[k] - y_out[k];

    transpose(kth_input, kth_input_transposed);
    multiply(kth_input_transposed, mu * e_out[k]);
    add(dw, kth_input_transposed, weights);

    destroy_signal(result);
    destroy_signal(dw);
    destroy_signal(kth_input_transposed);
    destroy_signal(kth_input);
  }

  destroy_signal(target_signal);
  destroy_signal(input_signal);
  destroy_signal(weights);
}

int main() {
  FILE* input_file = fopen("data/input.csv", "r");
  FILE* target_file = fopen("data/target.csv", "r");
  size_t length = 300000;
  double* input = malloc (length * 2 * sizeof(double));
  double* target = malloc (length * sizeof(double));

  for (size_t count = 0; count < length*2;) {
      int got = fscanf(input_file, "%lf %lf", &input[count], &input[count+1]);
      if (got != 2) break;
      count +=2;
  }
  fclose(input_file);

  for (size_t count = 0; count < length; count++) {
      int got = fscanf(target_file, "%lf", &target[count]);
      if (got != 1) break;
  }
  fclose(target_file);

  double* y= malloc (length * sizeof(double));
  double* e= malloc (length * sizeof(double));
  rls(target, input, 0.00001, 2, y, e, length);

  for(int i = 0; i < length; i++) {
    printf("y[%d]: [%.15f], e[%d]: [%.15f]\n", i, y[i], i, e[i]);
  }

  free(input);
  free(target);
  free(y);
  free(e);
}
