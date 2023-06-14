#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>

#define NUM_THREADS 10

int x = 0;
pthread_mutex_t mymutex = PTHREAD_MUTEX_INITIALIZER;

void *we_are_adding(void *arg) {
  int i;
  long int tid = (long int)arg;
  
  for (i=0; i<10000000; i++) {
#ifdef MUTEX
    pthread_mutex_lock(&mymutex);
#endif
    x = x + 1;
#ifdef MUTEX
    pthread_mutex_unlock(&mymutex);
#endif
  }
  
  printf("My thread ID is #%d and the value of x I see is %d (and my i is %d)\n", tid, x, i);
  pthread_exit(NULL);
}


int main() {
  pthread_t threads[NUM_THREADS];
  int ret = 0;
  long int t;
  
  for (t = 0; t<NUM_THREADS; t++) {
    ret = pthread_create(&threads[t], NULL, we_are_adding, (void *)t);
    if (ret) {
      printf("Error creating threads with code %d\n", ret);
      exit(-1);
    }
  }
  
  for(t = 0; t<NUM_THREADS; t++) {
    pthread_join(threads[t], NULL);
  }
  
  printf("I am the main thread and x for me is %d\n", x);
  pthread_exit(NULL);
  
  return 0;
}
