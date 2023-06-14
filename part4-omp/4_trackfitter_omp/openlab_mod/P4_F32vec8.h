#ifndef CBM_KF_F32vec8P4_H
#define CBM_KF_F32vec8P4_H

#include <stdlib.h>
#include <iostream>
#include <math.h>
//#include <xmmintrin.h>
#include <immintrin.h>
#include "../vec_arithmetic.h"

using namespace std;

/**********************************
 *
 *   Vector of four single floats
 *
 **********************************/

#pragma pack(push,16)/* Must ensure class & union 16-B aligned */

typedef __m256 VectorFloat __attribute__ ((aligned(16)));

const union
{
  float f;
  int i;
} __f_one = {(float)1.};

const union
{
    int i[8];
    __m256 m;
} 
__f32vec8_abs_mask_cheat = {0x7fffffff, 0x7fffffff, 0x7fffffff, 0x7fffffff, 0x7fffffff, 0x7fffffff, 0x7fffffff, 0x7fffffff},
__f32vec8_sgn_mask_cheat = {0x80000000, 0x80000000, 0x80000000, 0x80000000, 0x80000000, 0x80000000, 0x80000000, 0x80000000},
__f32vec8_zero_cheat     = {         0,          0,          0,          0,          0,          0,          0,          0},
__f32vec8_one_cheat      = {__f_one.i , __f_one.i , __f_one.i , __f_one.i, __f_one.i , __f_one.i , __f_one.i , __f_one.i },
__f32vec8_true_cheat     = {0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF, 0xFFFFFFFF},
__f32vec8_false_cheat    = {0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000, 0x00000000};

#define _f32vec8_abs_mask ((F32vec8)__f32vec8_abs_mask_cheat.m)
#define _f32vec8_sgn_mask ((F32vec8)__f32vec8_sgn_mask_cheat.m)
#define _f32vec8_zero     ((F32vec8)__f32vec8_zero_cheat.m)
#define _f32vec8_one      ((F32vec8)__f32vec8_one_cheat.m)
#define _f32vec8_true     ((F32vec8)__f32vec8_true_cheat.m)
#define _f32vec8_false    ((F32vec8)__f32vec8_false_cheat.m)

class F32vec8 
{
 public:

  __m256 v;

  float & operator[]( int i ){ return ((float*)&v)[i]; }
  float   operator[]( int i ) const { return ((float*)&v)[i]; }

  F32vec8( ){}
  F32vec8( const __m256 &a ) { v = a; }
  F32vec8( const float &a )         { v = _mm256_set1_ps(a); }

  F32vec8( const float &f0, const float &f1, const float &f2, const float &f3, const float &f4,const float &f5,const float &f6,const float &f7 ){ 
    v = _mm256_set_ps(f7, f6, f5, f4, f3,f2,f1,f0); 
  }

  /* Conversion function */
  operator  __m256() const { return v; }		/* Convert to __m256 */


  /* Arithmetic Operators */
  friend F32vec8 operator +(const F32vec8 &a, const F32vec8 &b) { return _mm256_add_ps(a,b); }
  friend F32vec8 operator -(const F32vec8 &a, const F32vec8 &b) { return _mm256_sub_ps(a,b); } 
  friend F32vec8 operator *(const F32vec8 &a, const F32vec8 &b) { return _mm256_mul_ps(a,b); } 
  friend F32vec8 operator /(const F32vec8 &a, const F32vec8 &b) { return _mm256_div_ps(a,b); }

  /* Functions */
  friend F32vec8 min( const F32vec8 &a, const F32vec8 &b ){ return _mm256_min_ps(a, b); }
  friend F32vec8 max( const F32vec8 &a, const F32vec8 &b ){ return _mm256_max_ps(a, b); }

  /* Square Root */
  friend F32vec8 sqrt ( const F32vec8 &a ){ return _mm256_sqrt_ps (a); }

  /* Reciprocal( inverse) Square Root */
  //friend F32vec8 rsqrt( const F32vec8 &a ){ return _mm256_rsqrt_ps(a); }
  friend F32vec8 rsqrt( const F32vec8 &a ){ return 1. / sqrt(a); }

  /* Reciprocal (inversion) */
  //friend F32vec8 rcp  ( const F32vec8 &a ){ return _mm256_rcp_ps  (a); }
  friend F32vec8 rcp  ( const F32vec8 &a ){ return 1. / a; }

  /* Absolute value */
  friend F32vec8 fabs(const F32vec8 &a){ return _mm256_and_ps(a, _f32vec8_abs_mask); }

  /* Sign */
  friend F32vec8 sgn(const F32vec8 &a){ return _mm256_or_ps(_mm256_and_ps(a, _f32vec8_sgn_mask),_f32vec8_one); }
  friend F32vec8 asgnb(const F32vec8 &a, const F32vec8 &b ){ 
    return _mm256_or_ps(_mm256_and_ps(b, _f32vec8_sgn_mask),a); 
  }

  /* Logical */
 
  friend F32vec8 operator&( const F32vec8 &a, const F32vec8 &b ){ // mask returned
    return _mm256_and_ps(a, b);
  }
  friend F32vec8 operator|( const F32vec8 &a, const F32vec8 &b ){ // mask returned
    return _mm256_or_ps(a, b);
  }
  friend F32vec8 operator^( const F32vec8 &a, const F32vec8 &b ){ // mask returned
    return _mm256_xor_ps(a, b);
  }
  friend F32vec8 operator!( const F32vec8 &a ){ // mask returned
    return _mm256_xor_ps(a, _f32vec8_true);
  }
  friend F32vec8 operator||( const F32vec8 &a, const F32vec8 &b ){ // mask returned
    return _mm256_or_ps(a, b);
  }

  /* Comparison */

  friend F32vec8 operator<( const F32vec8 &a, const F32vec8 &b ){ // mask returned
    return _mm256_cmp_ps(a, b, 1);	// imm == 1 ------> op <- lt_os
  }

  /* Non intrinsic functions */

#define _f1(A,F) F32vec8( F(A[0]), F(A[1]), F(A[2]), F(A[3]), F(A[4]), F(A[5]), F(A[6]), F(A[7]) ) 

  friend F32vec8 exp( const F32vec8 &a ){ return _f1( a, exp ); } 
  friend F32vec8 log( const F32vec8 &a ){ return _f1( a, log ); } 
  friend F32vec8 sin( const F32vec8 &a ){ return _f1( a, sin ); } 
  friend F32vec8 cos( const F32vec8 &a ){ return _f1( a, cos ); } 

#undef _f1

  /* Define all operators for consistensy */
  
  vec_arithmetic(F32vec8,float);

  friend ostream & operator<<(ostream &strm, const F32vec8 &a ){
    strm<<a[0]<<" "<<a[1]<<" "<<a[2]<<" "<<a[3]<<" "<<a[4]<<" "<<a[5]<<" "<<a[6]<<" "<<a[7];
    return strm;
  }

  friend istream & operator>>(istream &strm, F32vec8 &a ){
    float tmp;
    strm>>tmp;
    a = tmp;
    return strm;
  }

} __attribute__ ((aligned(16)));;


#endif 
