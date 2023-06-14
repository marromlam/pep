ICC=icc
GCC=gcc
CC=$(GCC)

OPT=-fopenmp
O0=$(OPT) -O0
O2=$(OPT) -O2
O3=$(OPT) -O3

LINK=-lm

TARGETS=primes

all: $(TARGETS)

primes: primes.c
	$(CC) $(LINK) $(OPT) $@.c -o $@

clean:
	rm -f *.o core.* *~ $(TARGETS)
