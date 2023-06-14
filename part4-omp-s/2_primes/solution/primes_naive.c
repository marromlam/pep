#include <stdio.h>
#include <math.h>
#include <stdbool.h>

bool primecheck(int n) {
  int i, limit = ceil(sqrt(n))+1;
  for(i=3; i<limit; i+=2)
    if (n % i == 0) return false;
  return true;
}

int main() {
  int i, max = 1e8;
  printf("1 2 ");

  #pragma omp parallel for  
  for(i=3; i<max; i+=2)
    if(primecheck(i)) printf("%d ", i);
    
  printf("\n");

  return 0;
}
