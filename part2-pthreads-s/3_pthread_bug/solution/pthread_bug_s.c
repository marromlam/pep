#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/syscall.h>

#define NUM_THREADS 4

int x = 0;

pthread_barrier_t barrier;

void *tokenize(void *arg) {
  int i;
  char *data = (char *)arg;
  char *save;
  int id = syscall(__NR_gettid);
  
  printf("Thread id %d received data: '%s'\n", id, data);
  char *result = NULL;
  
  pthread_barrier_wait(&barrier);
  
  result = strtok_r(data, " ", &save);
  printf("result[%d]: %s\n", id, result);
  result = strtok_r(NULL, " ", &save);
  printf("result[%d]: %s\n", id, result);
    
  pthread_exit(NULL);
}


int main() {
  pthread_t threads[NUM_THREADS];
  int ret = 0;
  long int t;
  
  char *m[NUM_THREADS];
  for(t=0; t<NUM_THREADS; t++) m[t] = malloc(100);

  sprintf(m[0], "%s", "Roses are red");
  sprintf(m[1], "%s", "Violets are blue");
  sprintf(m[2], "%s", "In this pthread program");
  sprintf(m[3], "%s", "Strings defeat you");

  ret = pthread_barrier_init(&barrier, NULL, NUM_THREADS);
  if (ret) {
    printf("Error initializing barrier with code %d\n", ret);
    exit(-1);
  }
  
  for (t = 0; t<NUM_THREADS; t++) {
    printf("Creating thread %d\n", t);
    ret = pthread_create(&threads[t], NULL, tokenize, (void *)m[t]);
    if (ret) {
      printf("Error creating threads with code %d\n", ret);
      exit(-1);
    }
  }
  
  for(t = 0; t<NUM_THREADS; t++) {
    pthread_join(threads[t], NULL);
  }
  
  printf("I'm the main thread and I'm saying goodbye\n");
  pthread_exit(NULL);
  
  return 0;
}
