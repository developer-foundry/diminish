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


  /** @brief Initialize a signal data structure @a signal containing
   * 
   * @a n the number of inputs to be adapted
   * @a len the length of each input
   *
   * Each siginal that is initialized with this function must be destroyed with a call to ::destroy_signal
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
   * @a n the number of inputs represented by signal
   * @a len the length of each signal
   **/
  void unmarshall(signal* signal, double* data, int n, int len);

  /** @brief Populate signal with zeros
   *
   * @a signal must have been initialized with a call to ::initialize_signal
   * @a n the number of inputs represented by signal
   * @a len the length of each signal
   **/
  void zeros(signal* signal, int n, int len);

  /** @brief Print signal for debugging purposes
   *
   * @a signal must have been initialized with a call to ::initialize_signal and contains data through ::unmarshall
   **/
  void print_signal(signal *signal);

#endif
