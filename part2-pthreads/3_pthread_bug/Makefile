ICC=icc
GCC=gcc
CC=$(GCC)

OPT=
O0=$(OPT) -O0
O2=$(OPT) -O2
O3=$(OPT) -O3

LINK=-lpthread

TARGETS=pthread_bug

all: $(TARGETS)

pthread_bug: pthread_bug.c
	$(CC) $(LINK) $(OPT) $@.c -o $@

clean:
	rm -f *.o core.* *~ $(TARGETS)
