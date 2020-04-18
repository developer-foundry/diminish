#ifndef FITLERING_H
  #define FILTERING_H 1

  #include <stddef.h>
  #include <stdio.h>
  #include <stdlib.h>
  #include <string.h>

  #define ANSI_COLOR_RED     "\x1b[31m"
  #define ANSI_COLOR_GREEN   "\x1b[32m"
  #define ANSI_COLOR_YELLOW  "\x1b[33m"
  #define ANSI_COLOR_BLUE    "\x1b[34m"
  #define ANSI_COLOR_MAGENTA "\x1b[35m"
  #define ANSI_COLOR_CYAN    "\x1b[36m"
  #define ANSI_COLOR_RESET   "\x1b[0m"
  
  #define EPS                0.1

  typedef struct signal signal;
  enum error_codes
  {
    E_SUCCESS = 0,
    E_INVALID_INPUT = 1,
    E_INVALID_MATRIX_DIMENSIONS = 2,
    E_OUT_OF_BOUNDS = 3
  };

  typedef enum error_codes error_t;
  struct _errordesc {
    int  code;
    char const*const message;
  } errordesc[] = {
    { E_SUCCESS, "No error"},
    { E_INVALID_INPUT, "Invalid input"},
    { E_INVALID_MATRIX_DIMENSIONS, "The number of columns and rows do not align for the matrix operation being performed"},
    { E_OUT_OF_BOUNDS, "The index given is out of the array bounds"}
  };

  /** @brief Return a human readable error message for @a error
   * 
   * @a error is an error_t ENUM
   * @return a human readable error message
   **/
  char const*const error_message(error_t error);

  /** @brief Initialize a signal data structure @a signal containing a multidimensional matrix using row major ordering
   * 
   * @a n the number of inputs to be adapted
   * @a len the length of each input
   * @return an initialized sigal that must be destroyed with a call to ::destroy_signal
   **/
  signal* initialize_signal(size_t n, size_t len);

  /** @brief Destroy signal @a signal
   *
   * @a signal must have been initialized with a call to ::initialize_signal
   **/
  void destroy_signal(signal* signal);

  /** @brief Populate input data into signal data structure
   *
   * @a signal must have been initialized with a call to ::initialize_signal
   * @a data the signal data to unmarshall into @a signal
   **/
  void unmarshall(signal* signal, double* data);

  /** @brief Extract a single row or sample from the input signal
   *
   * @a input must have been initialized with a call to ::initialize_signal
   * @a k is the index that is to be retrieved
   * @a result must have been initialized with a call to ::initialize_signal
   **/
  error_t extract(signal* input, int k, signal* result);

  /** @brief Populate signal with zeros
   *
   * @a signal must have been initialized with a call to ::initialize_signal
   **/
  void zeros(signal* signal);

  /** @brief Print signal for debugging purposes
   *
   * @a signal must have been initialized with a call to ::initialize_signal and contains data through ::unmarshall
   **/
  void print_signal(signal *signal);

  /** @brief Dot product between two signals
   *
   * @a a must have been initialized with a call to ::initialize_signal and contains data through ::unmarshall
   * @a b must have been initialized with a call to ::initialize_signal and contains data through ::unmarshall
   * @a adotb the result of a dot b - must have been initialized with a call to ::initialize_signal and contains data through ::unmarshall
   * @return an error ENUM in case an error code is returned
   **/
  error_t dot(signal* a, signal* b, signal* adotb);

  /** @brief Scalar multiplication of a signal. This performs in place and does not create a new signal
   *
   * @a a must have been initialized with a call to ::initialize_signal and contains data through ::unmarshall
   * @a multiplier scalar number to multiply against a inplace
   * @return an error ENUM in case an error code is returned
   **/
  error_t multiply(signal* a, double multiplier);

  /** @brief Scalar division of a signal. This performs in place and does not create a new signal
   *
   * @a a must have been initialized with a call to ::initialize_signal and contains data through ::unmarshall
   * @a divisor scalar number to divide against a inplace
   * @return an error ENUM in case an error code is returned
   **/
  error_t divide(signal* signal, double divisor);

  /** @brief Subtraction between two signals
   *
   * @a a must have been initialized with a call to ::initialize_signal and contains data through ::unmarshall
   * @a b must have been initialized with a call to ::initialize_signal and contains data through ::unmarshall
   * @a asubb the result of a subtract b - must have been initialized with a call to ::initialize_signal and contains data through ::unmarshall
   * @return an error ENUM in case an error code is returned
   **/
  error_t subtract(signal* a, signal* b, signal* asubb);

  /** @brief Addition between two signals
   *
   * @a a must have been initialized with a call to ::initialize_signal and contains data through ::unmarshall
   * @a b must have been initialized with a call to ::initialize_signal and contains data through ::unmarshall
   * @a aplusb the result of a plus b - must have been initialized with a call to ::initialize_signal and contains data through ::unmarshall
   * @return an error ENUM in case an error code is returned
   **/
  error_t add(signal* a, signal* b, signal* aplusb);

  /** @brief Signal transposition
   *
   * @a input must have been initialized with a call to ::initialize_signal and contains data through ::unmarshall
   * @a transposed must have been initialized with a call to ::initialize_signal and contains data through ::unmarshall
   * @return an error ENUM in case an error code is returned
   **/
  error_t transpose(signal* input, signal* transposed);

  /** @brief Least Means Squared adaptive filtering
   *
   * @a target_signal_in from python bindings - this is the desired output and is row major ordered
   * @a input_signal_in from python bindings - this is what the microphone is hearing and is row major ordered
   * @a mu from python bindings - this is the learning rate or step size
   * @a n from python bindings - this is the number of columns in the input signal
   * @a y_out from python bindings - this is an out parameter containing the output signal
   * @a e_out from python bindings - this is an out parameter containing the error signal
   * @a length from python bindings - this is the number of samples or rows in the input signal
   * 
   * Pseudo code version
   * y - output (Nx1 array)
   * e - error (Nx1 array)
   * w - weights (1xN array)
   * x - input signal (P x N array) - P is number of inputs and N is number of samples
   * d - target signal (1 x N array) - the desired output
   * 
   * y = np.zeros(N)
   * e = np.zeros(N)
   * for k in range(N):
   *   y[k] = np.dot(self.w, x[k])
   *   e[k] = d[k] - y[k]
   *   dw = self.mu * e[k] * x[k]
   *   self.w += dw
   * return y, e
   **/
  void lms(double *target_signal_in, double *input_signal_in, double mu, int n, double *y_out, double *e_out, int length);

  /** @brief Recursive Least Squares adaptive filtering
   *
   * @a target_signal_in from python bindings - this is the desired output and is row major ordered
   * @a input_signal_in from python bindings - this is what the microphone is hearing and is row major ordered
   * @a mu from python bindings - this is the learning rate or step size
   * @a n from python bindings - this is the number of columns in the input signal
   * @a y_out from python bindings - this is an out parameter containing the output signal
   * @a e_out from python bindings - this is an out parameter containing the error signal
   * @a length from python bindings - this is the number of samples or rows in the input signal
   * 
   * Pseudo code version
   * y - output (Nx1 array)
   * e - error (Nx1 array)
   * w - weights (1xN array)
   * x - input signal (P x N array) - P is number of inputs and N is number of samples
   * d - target signal (1 x N array) - the desired output
   * 
   * y = np.zeros(N)
   * e = np.zeros(N)
   * 
   * for k in range(N):
   *   y[k] = np.dot(self.w, x[k])
   *   e[k] = d[k] - y[k]
   *   R1 = np.dot(np.dot(np.dot(self.R,x[k]),x[k].T),self.R)
   *   R2 = self.mu + np.dot(np.dot(x[k],self.R),x[k].T)
   *   self.R = 1/self.mu * (self.R - R1/R2)
   *   dw = np.dot(self.R, x[k].T) * e[k]
   *   self.w += dw
   **/
  void rls(double *target_signal_in, double *input_signal_in, double mu, int n, double *y_out, double *e_out, int length);

#endif

/**
 * Examples of use
 */ 

/*int main() {
  int an = 8;
  int alen = 8;
  double* data = malloc (alen * an * sizeof(double));
  for (int i = 0; i < alen; i++) {
    for (int j = 0; j < an; j++) {
      data[j+i*an] = (double)(j+i*an);
    }
  }
  signal* a = initialize_signal(an, alen);
  unmarshall(a, data);
  print_signal(a);

  signal* extracted = initialize_signal(an, 1);
  error_t result = extract(a, 8, extracted);
  if(result == E_SUCCESS) {
    print_signal(extracted);
    printf("Success\n");
  }
  else {
    printf("Error %s\n", error_message(result));
  }

  int bn = 3;
  int blen = 3;
  free(data);
  data = malloc (blen * bn * sizeof(double));
  for (int i = 0; i < blen; i++) {
    for (int j = 0; j < bn; j++) {
      data[j+i*bn] = (double)(j+i*bn);
    }
  }
  signal* b = initialize_signal(bn, blen);
  unmarshall(b, data);
  free(data);
  print_signal(b);

  signal* adotb = initialize_signal(bn, alen);
  error_t result = dot(a, b, adotb);
  if(result == E_SUCCESS) {
    print_signal(adotb);
    printf("Success\n");
  }
  else {
    printf("Error %s\n", error_message(result));
  }

  result = multiply(a, 2);
  if(result == E_SUCCESS) {
    print_signal(a);
    printf("Success\n");
  }
  else {
    printf("Error %s\n", error_message(result));
  }

  result = divide(a, 2);
  if(result == E_SUCCESS) {
    print_signal(a);
    printf("Success\n");
  }
  else {
    printf("Error %s\n", error_message(result));
  }

  signal* asubb = initialize_signal(an, alen);
  result = subtract(a, b, asubb);
  if(result == E_SUCCESS) {
    print_signal(asubb);
    printf("Success\n");
  }
  else {
    printf("Error %s\n", error_message(result));
  }

  signal* aplusb = initialize_signal(an, alen);
  result = add(a, b, aplusb);
  if(result == E_SUCCESS) {
    print_signal(aplusb);
    printf("Success\n");
  }
  else {
    printf("Error %s\n", error_message(result));
  }

  signal* atransposed = initialize_signal(alen, an);
  result = transpose(a, atransposed);
  if(result == E_SUCCESS) {
    print_signal(atransposed);
    printf("Success\n");
  }
  else {
    printf("Error %s\n", error_message(result));
  }

  destroy_signal(a);
  destroy_signal(b);
  destroy_signal(adotb);
  destroy_signal(asubb);
  destroy_signal(aplusb);
  destroy_signal(atransposed);
  destroy_signal(extracted);

  return 0;
}*/
