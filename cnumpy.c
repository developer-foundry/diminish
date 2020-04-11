#include <stdio.h>

float cnumpy(float* arr, int length) {
  printf("Here in function\n");
  for(int i = 0; i < length; i++) {
    printf("%d - %f\n", i, *arr);
    arr++;
  }
  printf("returning function\n");
  return 0.0;
}
