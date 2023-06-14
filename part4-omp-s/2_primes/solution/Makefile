ICC=icc
GCC=gcc
CC=$(GCC)

OPT=-fopenmp
O0=$(OPT) -O0
O2=$(OPT) -O2
O3=$(OPT) -O3

LINK=-lm

TARGETS=primes_naive

all: $(TARGETS)

primes_naive: primes_naive.c
	$(CC) $(LINK) $(OPT) $@.c -o $@

clean:
	rm -f *.o core.* *~ $(TARGETS)
