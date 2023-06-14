#include <stdio.h>
#include <omp.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
  if (argc != 2) {
    printf("Incorrect number of arguments.\n");
    exit(-1);
  }

  int N = atoi(argv[1]);
  
  #pragma omp parallel num_threads(N)
  printf("[thread %3d] Hello, world!\n", omp_get_thread_num());

  #pragma omp parallel
  printf("[thread %3d] Everybody!\n", omp_get_thread_num());

  #pragma omp parallel num_threads(4)
  printf("Goodbye, world!\n");
  
  return 0;
}
