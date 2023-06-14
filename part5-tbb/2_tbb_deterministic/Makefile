ICC=icc
GCC=gcc
CC=$(ICC)

OPT=-std=c++11
O0=$(OPT) -O0
O2=$(OPT) -O2
O3=$(OPT) -O3

LINK=-ltbb

TARGETS=det_reduce

all: $(TARGETS)

det_reduce: det_reduce.cpp
	$(CC) $(LINK) $(OPT) $@.cpp -o $@

clean:
	rm -f *.o core.* *~ $(TARGETS)
