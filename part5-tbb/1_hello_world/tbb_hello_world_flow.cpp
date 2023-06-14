/* with code from the Intel website */

#include <iostream>
#include "tbb/flow_graph.h"

using namespace std;
using namespace tbb;
using namespace tbb::flow;

int main(int argc, char *argv[]) {
  graph g;
  
  // TODO
  continue_node<continue_msg> n1(...);
  continue_node<continue_msg> n2(...);
  
  // TODO: add an edge and send a message to the first node
  
  return 0;
}
