# define KNF to compile for KNF, otherwise compile for CPU only
# Values: direct, offload
#KNF=direct
#KNF=offload

TBB=yes
CEAN=yes
CILK=yes

##MPI=mpiicpc
#MPI=mpic++
#TAU=yes

DIR       = XEON

BITS      = -m64
CXXFLAGS  = -O2 $(BITS) -fPIC -funroll-loops -finline-functions
#-fp-model precise -fp-model source -fimf-precision=high
# -no-prec-div -fast-transcendentals
#CXXFLAGS  = -O3 $(BITS) -fPIC -funroll-all-loops -finline-functions -ipo -no-prec-div -fast-transcendentals -xHost
# -debug all
SOFLAGS  = -shared
# Add Minuit2 directory
INCLUDE  = -I../Minuit2/include/
SOLIBS   = -L../Minuit2/lib -lMinuit2 -Wl,-rpath=./:../Minuit2/lib

ifdef KNF
CXX       = icpc
ifeq  ($(KNF),direct)
LDFLAGS   = -limf -lsvml -lintlc
CXXFLAGS += -mmic -no-fma 
#-fimf-accuracy-bits=22
#:exp
#CXXFLAGS += -no-vec
INCLUDE  = -I../Minuit2/MIC/include/
SOLIBS   = -L../Minuit2/MIC/lib -lMinuit2 -Wl,-rpath=./:../Minuit2/MIC/lib
DIR      = MIC
else
CXXFLAGS  += -offload-build -opt-report-phase:offload -offload-copts:"$(INCLUDE) -vec-report=3"
#LDFLAGS    = -offload-ldopts:"-v -Wl,-no-undefined -L/opt/intel/composerxe_mic-12.0.0.025/compiler/lib/mic -lcprts -lcxa -lunwind"
#LDFLAGS    = -offload-ldopts:"libMainLRB.out"
endif
else
#CXX       = g++
CXX       = icpc
# Vectorization
#CXXFLAGS  += -msse3
#CXXFLAGS  += -xSSE4.2
CXXFLAGS  += -axAVX
#CXXFLAGS  += -mavx
#CXXFLAGS  += -xSSE4.2 -fp-model extended -fimf-precision=high
#CXXFLAGS   += -mia32
#CXXFLAGS  += -no-vec
#CXXFLAGS  += -guide-vec
LDFLAGS   = -ldl
endif

INCLUDE   += -I$(PWD)
CXXWARN   = -Wall
OPENMP    = -fopenmp

# Note: CUDA uses g++ as default compiler for the host
ifeq ($(CXX),icpc)     
CXXFLAGS  += -ip -vec-report1 
#-mkl=sequential
#-g -openmp-link dynamic
CXXWARN    = -w1 -Wall -wd654
OPENMP     = -openmp -openmp-report2
#CXXFLAGS  += -ansi-alias
#LDFLAGS   += -L$(MKLROOT)/lib/intel64 -lmkl_intel_lp64 -lmkl_sequential -lmkl_core -lpthread -lm
ifdef TBB
CXXFLAGS  += -DUSE_TBB -tbb
LDFLAGS   += -ltbbmalloc
endif
ifdef CEAN
CXXFLAGS  += -DUSE_CEAN
endif
ifdef CILK
CXXFLAGS  += -DUSE_CILK 
#-cilk-serialize
endif
else
CXXFLAGS  += -mfpmath=sse -ftree-vectorize -ftree-vectorizer-verbose=1
endif

ifdef MPI
CXX        = $(MPI)
CXXFLAGS  += -DUSE_MPI
ifeq ($(MPI),mpiicpc)
ifndef TAU
CXXFLAGS  += -mt_mpi
endif
endif

ifdef TAU
CXX        = tau_cxx.sh
include $(TAU_MAKEFILE)
CXXFLAGS  += -optTauCC="$(TAU_CCOMPILER) -fPIC"
ifeq ($(MPI),mpiicpc)
CXXFLAGS  += -DMPICH_IGNORE_CXX_SEEK
endif
endif

endif


MAIN    := main
LIB     := libMain_$(DIR).so
CXXLIST := $(filter-out $(MAIN).cxx,$(wildcard *.cxx))
HHLIST  := $(filter-out common.h, $(patsubst %.cxx,%.h,$(CXXLIST)))
OBJLIST := $(patsubst %.cxx,$(DIR)/%.o,$(CXXLIST))

.SUFFIXES: .cxx .o .h .so

all: $(MAIN)_$(DIR)

$(DIR)/%.o: %.cxx %.h
	@echo "Compiling $<"
	@mkdir -p $(DIR)
	$(CXX) $(CXXFLAGS) $(CXXWARN) $(OPENMP) $(ROOTINC) $(INCLUDE) -c $< -o $@

$(LIB): $(OBJLIST)
	@echo "Making library..."
	$(CXX) $(CXXFLAGS) $(CXXWARN) $(OPENMP) $(SOLIBS) $(SOFLAGS) $^ -o $@

$(MAIN)_$(DIR): $(MAIN).cxx $(LIB) models/*.h
	@echo "Making executable..."
	$(CXX) $(CXXFLAGS) $(CXXWARN) $(OPENMP) $(ROOTINC) $(INCLUDE) $(ROOTLIB) $(SOLIBS) $< $(LIB) -o $@ $(LDFLAGS)

valgrind:
	valgrind --tool=callgrind --simulate-cache=yes --collect-jumps=yes --separate-threads=yes --simulate-hwpref=yes --cacheuse=yes ./main -n 100000

clean:
	rm -rf *~ */*~ *.o *.out *.xnlog $(LIB) $(MAIN)_$(DIR) *.inc *.pomp.* $(DIR)/
