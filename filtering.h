#ifndef FITLERING_H
  #define FILTERING_H 1

  #include <stddef.h>
  #include <stdio.h>
  #include <stdlib.h>

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
    E_INVALID_MATRIX_DIMENSIONS = 2
  };

  typedef enum error_codes error_t;
  struct _errordesc {
    int  code;
    char const*const message;
  } errordesc[] = {
    { E_SUCCESS, "No error"},
    { E_INVALID_INPUT, "Invalid input"},
    { E_INVALID_MATRIX_DIMENSIONS, "The number of columns from matrix a do not equal the number of rows of matrix b"}
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

#endif
