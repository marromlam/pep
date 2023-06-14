ICC=icc
GCC=gcc
CC=$(GCC)

OPT=
O0=$(OPT) -O0
O2=$(OPT) -O2
O3=$(OPT) -O3

LINK=-lpthread

TARGETS=bad_pthreads

all: $(TARGETS)

bad_pthreads: bad_pthreads.c
	$(CC) $(LINK) $(OPT) $@.c -o $@

clean:
	rm -f *.o core.* *~ $(TARGETS)
