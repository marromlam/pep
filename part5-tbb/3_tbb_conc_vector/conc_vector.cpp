/* 
naive concurrent vector sample

also see https://software.intel.com/en-us/videos/1-minute-intro-intel-tbb-concurrent-vector
*/

#include <iostream>
#include <vector>
#include <stdio.h>

#include "tbb/parallel_for.h"
#include "tbb/parallel_reduce.h"
#include "tbb/blocked_range.h"
#include "tbb/concurrent_vector.h"
#include "tbb/tick_count.h"

#define SIZE 10000000

using namespace std;
using namespace tbb;

class VecItem {
  int id;
  string contents;
  
  public:
    VecItem(int initial_id=0, char *initial_contents=NULL) {
      id = initial_id;
      if (initial_contents)
        contents = string(initial_contents);
      else
        contents = string("empty");
    }
    
    void do_work() {
      for(int i=0; i<contents.length(); i++) contents[i] += 3;
    }
    
    void print() {
      cout << "   Item " << id << ": /" << contents << "/" << endl;
    }
};

// TODO: make sure you have a way to measure time

int main(int argc, char *argv[]) {
  std::vector<VecItem> stdvec;
  std::vector<VecItem>::iterator item;
  tbb::concurrent_vector<VecItem> tbbvec;
  tbb::concurrent_vector<VecItem>::iterator tbb_item;
  
  int j = 0;
  char proxy[128];

  cout << "Initializing data" << endl;
  // TODO: measure the performance of these operations  
  stdvec.resize(SIZE);
  for(item=stdvec.begin(); item != stdvec.end(); item++, j++) {
    sprintf(proxy, "hello world, message #%d", j);
    *item = VecItem(j, proxy);
  }

  // TODO: measure the performance of these operations  
  j = 0;
  tbbvec.grow_by(SIZE);
  for(tbb_item=tbbvec.begin(); tbb_item != tbbvec.end(); tbb_item++, j++) {
    sprintf(proxy, "hello world, message #%d", j);
    *tbb_item = VecItem(j, proxy);
  }

  cout << "std::vector" << endl;
  stdvec[0].print();
  stdvec[SIZE-1].print();

  cout << "tbb::concurrent_vector" << endl;
  tbbvec[0].print();
  tbbvec[SIZE-1].print();

  cout << "Processing data" << endl;
  // TODO: serial version with stdvec
  
  // TODO: serial version with tbbvec
  
  // TODO: parallel version with tbbvec
//  tbb::parallel_for(...)

  cout << "std::vector" << endl;
  stdvec[0].print();
  stdvec[SIZE-1].print();

  cout << "tbb::concurrent_vector" << endl;
  tbbvec[0].print();
  tbbvec[SIZE-1].print();
  
  return 0;
}
