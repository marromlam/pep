ICC=icc
GCC=gcc
CC=$(ICC)

OPT=-std=c++11
O0=$(OPT) -O0
O2=$(OPT) -O2
O3=$(OPT) -O3

LINK=-ltbb

TARGETS=conc_vector

all: $(TARGETS)

conc_vector: conc_vector.cpp
	$(CC) $(LINK) $(OPT) $@.cpp -o $@

clean:
	rm -f *.o core.* *~ $(TARGETS)
