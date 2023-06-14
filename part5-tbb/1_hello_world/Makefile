ICC=icc
GCC=gcc
CC=$(ICC)

OPT=-std=c++11
O0=$(OPT) -O0
O2=$(OPT) -O2
O3=$(OPT) -O3

LINK=-ltbb

TARGETS=tbb_hello tbb_hello_world_flow

all: $(TARGETS)

tbb_hello: tbb_hello.cpp
	$(CC) $(LINK) $(OPT) $@.cpp -o $@

tbb_hello_world_flow: tbb_hello_world_flow.cpp
	$(CC) $(LINK) $(OPT) $@.cpp -o $@
        
clean:
	rm -f *.o core.* *~ $(TARGETS)
