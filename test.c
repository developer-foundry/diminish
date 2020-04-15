#include <stdio.h>
#include <stdarg.h>

int main() {
  //data = *(base + a * (b x h) + b * (h) + c);
  for (int i = 0; i < 4; i++) {
    printf("sample %d: [", i);
    for (int j = 0; j < 10; j++) {
      if(j < 9)
        printf("%d,", j+i*9+i);
      else
        printf("%d", j+i*9+i);
    }
    printf("]\n");
  }

  return 0;
}