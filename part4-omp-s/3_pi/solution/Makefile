ICC=icc
GCC=gcc
CC=$(GCC)

OPT=-fopenmp
O0=$(OPT) -O0
O2=$(OPT) -O2
O3=$(OPT) -O3

LINK=-lm

TARGETS=pi_numint

all: $(TARGETS)

pi_numint: pi_numint.c
	$(CC) $(LINK) $(OPT) $@.c -o $@

clean:
	rm -f *.o core.* *~ $(TARGETS)
