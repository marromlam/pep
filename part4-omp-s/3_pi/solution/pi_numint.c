#include <stdio.h>
#include <math.h>

#define REAL_PI 3.141592653589793238462643383279502884197169399375105820974944592

int main() {
  long int i, steps = 1e10;
  double result = 0, step = 1./steps;
  char format[100];
  
  #pragma omp parallel for reduction(+:result)
  for(i=0; i<steps; i++) {
    result += 4./(1.+step*step*(i+0.5)*(i+0.5));
  }
  
  printf("Result : %.50f\n", result*step);
  printf("Real PI: %.50f\n", REAL_PI);
  printf("Error  : %.20f\n", fabs(REAL_PI-result*step));
  printf("Error  : 10e%.f\n", log10(fabs(REAL_PI-result*step)));

  return 0;
}
