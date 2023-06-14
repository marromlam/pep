#define NOMINMAX
#define _CRT_SECURE_NO_WARNINGS

#include <algorithm>
// GNU C++ 4.5.1 or later, or VS2010 or later, are known to support std::move
#if (__GNUC__*10000+__GNUC_MINOR__*100+__GNUC_PATCHLEVEL__)>=40501 || _MSC_VER>=1600
#include <utility>
#define HAVE_MOVE 1
#else
namespace std {
// Declare fake "move"
template<typename T> T& move( T& x ) {return x;}
template<typename T> T* move( const T* xs, const T* xe, T* ys ) {return std::copy(xs,xe,ys);}
}
#endif

#include <tbb/tbb.h>
#include <cstdio>
#include <cstdlib>
#include <cassert>

#define CHECK_STABILITY 1
#define EXPONENTIAL_DISTRIBUTION 2
#define UNIFORM_DISTRIBUTION 3
#define STRING_KEY 4

//#define MODE STRING_KEY
#define MODE UNIFORM_DISTRIBUTION
//#define MODE CHECK_STABILITY

unsigned Random() {
    return rand()*(RAND_MAX+1u)+rand();
}

const char SequenceName[] = "uniform distribution of int";

typedef int T;

inline T MakeRandomT( size_t ) {return Random();}

#include "quicksort_util.h"
#include "sample_sort_util.h"

namespace Ex0 {
#include "serial_merge.h"
}

namespace Ex5 {         // TBB semi-recursive quicksort using task_group
#include "quicksort_tbb_taskgroup.h"
}

// For comparing with STL sort
namespace Ref {

void stl_sort( T* first, T* last ) {
    std::sort(first,last);
}

}

void TestSerialMerge( void (*mergeRoutine)( T* xs, T* xe,  T* ys, T* ye, T* zs )  ) {
    const size_t n = 10;
    T x[2][n], z[2*n], w[2*n];
    size_t m[2];
    for( m[0]=0; m[0]<n; ++m[0] )
        for( m[1]=0; m[1]<n; ++m[1] ) {
            for( size_t i=0; i<2; ++i ) {
                for( size_t j=0; j<m[i]; ++j ) 
                    x[i][j] = MakeRandomT(j); 
                std::sort(x[i],x[i]+m[i]);
            }
            (*mergeRoutine)( x[0], x[0]+m[0], x[1], x[1]+m[1], z );
            std::merge( x[0], x[0]+m[0], x[1], x[1]+m[1], w );
            for( int k=0; k<m[0]+m[1]; ++k ) {
                assert( !(z[k]<w[k]||w[k]<z[k]) );
#if MODE==CHECK_STABILITY
                assert( IndexOf(z[k])==IndexOf(w[k]) );
#endif
            }
        }
}

// Big defaults for timing
size_t M = 10;
size_t N = 1000000;

T *Unsorted, *Expected, *Actual;

void InitializeTestData() {
    Unsorted = new T[M*N];
    Expected = new T[M*N];
    Actual = new T[M*N];
    for( size_t i=0; i<M; ++i ) {
        for( size_t j=0; j<N; ++j ) {
            Unsorted[i*N+j] = MakeRandomT(j); 
        }
        std::copy( Unsorted+i*N, Unsorted+(i+1)*N, Expected+i*N );
        std::stable_sort( Expected+i*N, Expected+(i+1)*N );
    }
}

template<typename S> 
void TestSort( S sortToBeTested, const char* what, bool shouldBeStable=false ) {
    std::copy( Unsorted, Unsorted+M*N, Actual );
    // Warm up run-time
    sortToBeTested(Actual,Actual+N);
    tbb::tick_count t0 = tbb::tick_count::now();
    for( int i=1; i<M; ++i ) {
#if MODE==CHECK_STABILITY
        KeyCount=0;
#endif
        sortToBeTested(Actual+i*N,Actual+(i+1)*N);
#if MODE==CHECK_STABILITY
        assert(KeyCount==0);
#endif
    }
    tbb::tick_count t1 = tbb::tick_count::now();
    for( size_t k=0; k<M*N; ++k ) {
        if(Actual[k]<Expected[k] || Expected[k]<Actual[k]) {
            printf("Error for %s\n",what);
            return;
        }
#if MODE==CHECK_STABILITY
        if( shouldBeStable ) {
            if( IndexOf(Actual[k])!=IndexOf(Expected[k]) ) {
                printf("Stability error for %s\n",what);
                return;
            }
        }
#endif /* MODE==CHECK_STABILITY */
    }
    printf("%30s\t%5.2f\n",what,(t1-t0).seconds());
}

template<void (*F)(T*,T*,T*,bool)>
void call_parallel_merge_sort( T* xs, T* xe ) {
    T* zs = new T[xe-xs];
    (*F)( xs, xe, zs, true );
    delete[] zs;
}

int main( int argc, char* argv[] ) {
    if( argc>1 ) M = strtol(argv[1],0,0);
    ++M;    // Add one for the warmup sort
    if( argc>2 ) N = strtol(argv[2],0,0);
    srand(2);

    // Serial merge routine is not used elsewhere, so it needs to be tested separately.
    TestSerialMerge( Ex0::serial_merge );

    InitializeTestData();
    std::printf("Testing for %d sorts of length %d for %s\n",int(M-1),int(N),SequenceName);\
    
    // Test serial sort
    TestSort(Ref::stl_sort,"STL sort");

    // Test TBB sort
    TestSort(Ex5::parallel_quicksort,"TBB quicksort taskgroup");

    std::printf("Done\n");
}
