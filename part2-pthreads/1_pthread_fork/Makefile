ICC=icc
GCC=gcc
CC=$(GCC)

OPT=
O0=$(OPT) -O0
O2=$(OPT) -O2
O3=$(OPT) -O3

LINK=-lpthread

TARGETS=pt_fork pt_pt

all: $(TARGETS)

pt_fork: pt_fork.c
	$(CC) $(LINK) $(OPT) $@.c -o $@

pt_pt: pt_pt.c
	$(CC) $(LINK) $(OPT) $@.c -o $@

clean:
	rm -f *.o core.* *~ $(TARGETS)
