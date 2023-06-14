/* deterministic reductions; with code from the Intel website */

#include <iostream>
#include <vector>

#include "tbb/parallel_reduce.h"
#include "tbb/blocked_range.h"

#define REPEAT 10
#define N 1000

using namespace std;
using namespace tbb;

struct Sum {
    float value;
    Sum() : value(0) {}
    Sum( Sum& s, split ) {value = 0;}
    void operator()( const blocked_range<float*>& r ) {
        float temp = value;
        for( float* a=r.begin(); a!=r.end(); ++a ) {
            temp += *a;
        }
        value = temp;
    }
    void join( Sum& rhs ) {value += rhs.value;}
};

float ParallelSum( float array[], size_t n ) {
    Sum total;
    parallel_reduce( blocked_range<float*>( array, array+n ),
                     total );
    return total.value;
}

float ParallelDetSum( float array[], size_t n ) {
    Sum total;
    parallel_deterministic_reduce( blocked_range<float*>( array, array+n ),
                     total );
    return total.value;
}

int main(int argc, char *argv[]) {

  float arr[N];
  for (int i=0; i<N; i++) arr[i] = 1.0f/(float)N;

  cout << "Making parallel reductions" << endl;  
  for (int i=0; i<REPEAT; i++) {
    cout << ParallelSum(arr, N) << endl;
  }

  cout << "Making deterministic parallel reductions" << endl;  
  for (int i=0; i<REPEAT; i++) {
    cout << ParallelDetSum(arr, N) << endl;
  }

  return 0;
}
