#ifndef CBM_KF_F64vec4P4_H
#define CBM_KF_F64vec4P4_H

#include <stdlib.h>
#include <iostream>
#include <math.h>
#include <immintrin.h>
#include "../vec_arithmetic.h"

using namespace std;

/**********************************
 *
 *   Vector of four double floats (AVX)
 *
 **********************************/

#pragma pack(push,16)/* Must ensure class & union 16-B aligned */

typedef __m256d VectorDouble __attribute__ ((aligned(16)));

const union
{
  double f;
  long long i;
} __f_one = {(double)1.};

const union
{
    int i[8];
    __m256d m;
} 
//__f64vec2_abs_mask_cheat = {0xffffffff, 0x7fffffff, 0x7fffffff, 0x7fffffff},
__f64vec4_sgn_mask_cheat = {0x80000000, 0x80000000, 0x80000000, 0x80000000, 0x80000000, 0x80000000, 0x80000000, 0x80000000},
//__f64vec2_sgn_mask_cheat = {0x8000000000000000, 0x8000000000000000},
//__f64vec2_zero_cheat     = {         0,          0,          0,          0},
//__f64vec2_one_cheat      = {__f_one.i , __f_one.i , __f_one.i , __f_one.i },
__f64vec4_one_cheat      = {(double)1., (double)1., (double)1., (double)1.},
//__f64vec2_one_cheat      = {__f_one.i, __f_one.i},
__f64vec4_true_cheat     = {0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF};
//__f64vec2_false_cheat    = {0x00000000, 0x00000000, 0x00000000, 0x00000000};


//#define _f64vec4_abs_mask ((F64vec4)__f64vec4_abs_mask_cheat.m)
#define _f64vec4_sgn_mask ((F64vec4)__f64vec4_sgn_mask_cheat.m)
#define _f64vec4_zero     ((F64vec4)__f64vec4_zero_cheat.m)
#define _f64vec4_one      ((F64vec4)__f64vec4_one_cheat.m)
#define _f64vec4_true     ((F64vec4)__f64vec4_true_cheat.m)
#define _f64vec4_false    ((F64vec4)__f64vec4_false_cheat.m)

class F64vec4 
{
 public:

  __m256d v;

  double & operator[]( int i ){ return ((double*)&v)[i ]; }
  double   operator[]( int i ) const { return ((double*)&v)[i ]; }

  F64vec4( ){}
  F64vec4( const __m256d &a ) { v = a; }
  F64vec4( const double &a )         { v = _mm256_set1_pd(a); }
  //F64vec4( const double &a )         { v = _mm_set_pd1(a); }

  F64vec4( const double &f0, const double &f1, const double &f2, const double &f3){ 
    v = _mm256_set_pd(f3, f2, f1, f0); 
  }

  /* Conversion function */
  operator  __m256d() const { return v; }		/* Convert to __m256d */

  /* Arithmetic Operators */
  friend F64vec4 operator +(const F64vec4 &a, const F64vec4 &b) { return _mm256_add_pd(a,b); }
  friend F64vec4 operator -(const F64vec4 &a, const F64vec4 &b) { return _mm256_sub_pd(a,b); }
  friend F64vec4 operator *(const F64vec4 &a, const F64vec4 &b) { return _mm256_mul_pd(a,b); }
  friend F64vec4 operator /(const F64vec4 &a, const F64vec4 &b) { return _mm256_div_pd(a,b); }

  /* Functions */
  friend F64vec4 min( const F64vec4 &a, const F64vec4 &b ){ return _mm256_min_pd(a, b); }
  friend F64vec4 max( const F64vec4 &a, const F64vec4 &b ){ return _mm256_max_pd(a, b); }

  /* Square Root */
  friend F64vec4 sqrt ( const F64vec4 &a ){ return _mm256_sqrt_pd (a); }

  /* Reciprocal( inverse) Square Root */
  /* Intrinsic does not exist for double */
  friend F64vec4 rsqrt( const F64vec4 &a ){ return 1. / sqrt(a); }
  //friend F64vec4 rsqrt( const F64vec4 &a ){ return _f64vec4_one / _mm_sqrt_pd(a); }

  /* Reciprocal (inversion) */
  /* Intrinsic does not exist for double */
  friend F64vec4 rcp  ( const F64vec4 &a ){ return 1. / a; }
  //friend F64vec4 rcp  ( const F64vec4 &a ){ return _f64vec4_one / a; }

  /* Absolute value */
//  friend F64vec4 fabs(const F64vec4 &a){ return _mm_and_pd(a, _f64vec4_abs_mask); }

  /* Sign */
  friend F64vec4 sgn(const F64vec4 &a){ return _mm256_or_pd(_mm256_and_pd(a, _f64vec4_sgn_mask),_f64vec4_one); }
  friend F64vec4 asgnb(const F64vec4 &a, const F64vec4 &b ){ 
    return _mm256_or_pd(_mm256_and_pd(b, _f64vec4_sgn_mask),a); 
  }

  /* Logical */
 
  friend F64vec4 operator&( const F64vec4 &a, const F64vec4 &b ){ // mask returned
    return _mm256_and_pd(a, b);
  }
  friend F64vec4 operator|( const F64vec4 &a, const F64vec4 &b ){ // mask returned
    return _mm256_or_pd(a, b);
  }
  friend F64vec4 operator^( const F64vec4 &a, const F64vec4 &b ){ // mask returned
    return _mm256_xor_pd(a, b);
  }
  friend F64vec4 operator!( const F64vec4 &a ){ // mask returned
    return _mm256_xor_pd(a, _f64vec4_true);
  }
  friend F64vec4 operator||( const F64vec4 &a, const F64vec4 &b ){ // mask returned
    return _mm256_or_pd(a, b);
  }

  /* Comparison */

  friend F64vec4 operator<( const F64vec4 &a, const F64vec4 &b ){ // mask returned
//---    return _mm_cmplt_pd(a, b);
    return _mm256_cmp_pd(a, b, 1);	// imm == 1 ----> OP <- LT_OS
  }

  /* Non intrinsic functions */

#define _f1(A,F) F64vec4( F(A[0]), F(A[1]), F(A[2]), F(A[3])) 

  friend F64vec4 exp( const F64vec4 &a ){ return _f1( a, exp ); } 
  friend F64vec4 log( const F64vec4 &a ){ return _f1( a, log ); } 
  friend F64vec4 sin( const F64vec4 &a ){ return _f1( a, sin ); } 
  friend F64vec4 cos( const F64vec4 &a ){ return _f1( a, cos ); } 

#undef _f1

  /* Define all operators for consistensy */
  
  vec_arithmetic(F64vec4,float);

  friend ostream & operator<<(ostream &strm, const F64vec4 &a ){
    strm<<a[0]<<" "<<a[1]<<" "<<a[2]<<" "<<a[3];
    //strm<<a[0]<<" "<<a[1]<<" "<<a[2]<<" "<<a[3];
    return strm;
  }

  friend istream & operator>>(istream &strm, F64vec4 &a ){
    float tmp;
    strm>>tmp;
    a = tmp;
    return strm;
  }

} __attribute__ ((aligned(16)));;


#endif 
