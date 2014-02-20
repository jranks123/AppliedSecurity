#include "modmul.h"
#include <gmp.h>
#include "math.h"


 #define max(a,b) \
   ({ __typeof__ (a) _a = (a); \
       __typeof__ (b) _b = (b); \
     _a > _b ? _a : _b; })

/*
Perform stage 1:

- read each 3-tuple of N, e and m from stdin,
- compute the RSA encryption c,
- then write the ciphertext c to stdout.
*/


/*void mAryFixedRecode(mpz_t y, int k){
    size_t nx = mpz_size( y );
    gmp_printf("Y = %Zx\n", y);
    gmp_printf("size - %d\n", nx);
    int i;
    mp_limb_t tx[ nx ];
    mpz_export( tx, NULL, -1, sizeof( mp_limb_t ), -1, 0, y);
    for (i = 0; i<nx; i++){
        gmp_printf( "%d -  %llu\n",i, tx[i] );
    }
}


void mAryFixed(mpz_t result, mpz_t x, mpz_t y, mpz_t N){
    int k = 2;
    mAryFixedRecode(y, k);

}*/

    //mpz_tstbit

void calculateT(int tSize, mpz_t* T, mpz_t x, mpz_t N){
    int i = 0;
    int k = 0;
    mpz_t xSquared;
    mpz_inits(T[0], xSquared, NULL);
    mpz_set(T[0], x);
    mpz_mul(xSquared, x, x);
    mpz_mod(xSquared, xSquared, N);  
    for(i = 1; i < tSize; i++){
      mpz_init(T[i]);
      mpz_mul(T[i], T[i-1], xSquared);
      mpz_mod(T[i], T[i], N);  
    }
    mpz_clear(xSquared);
}

void newPow(mpz_t t, mpz_t x, mpz_t y, mpz_t N){
  int k = 6;
  double m = pow(2,k);
  size_t tSize = round(m/2);
  mpz_t T[tSize];
  calculateT(tSize, T, x, N);
  mpz_init(t);
  mpz_set_ui(t, 1);
  int i = mpz_sizeinbase (y, 2) -1;
  size_t l, u;
  int e, c, g;
  while(i >= 0){
      if(mpz_tstbit(y, i) == 0){
         l = i; u = 0;
      }else{
        l = max(i-k+1, 0);
        while(mpz_tstbit(y, l) == 0){
          l += 1;
        }
        u = 0; 
        e = 1;
        for(c = l; c <= i; c++){
          if(mpz_tstbit(y, c) == 1){
              u+=e;
          }
          e = e<<1;
        }
      }
      for(g = 0; g < i-l+1; g++){
        mpz_mul(t, t, t);
        mpz_mod(t, t, N);
      }

        if(u != 0){
            size_t q = (u-1)/2;
            mpz_mul(t,t,T[q]);
            mpz_mod(t,t,N);
        }
      i = l-1;
    }

   for(i = 0; i < tSize; i++){
      mpz_clear( T[i] );
  }
}


void test() {
  // fill in this function with solution
    mpz_t N, e, m, c;
    int lineCount = 0;
    mpz_inits(N,e,m,c,NULL);
    do{
      lineCount = gmp_scanf( "%Zx\n%Zx\n%Zx", N, e, m );
       if(lineCount == 3){
        newPow(c,m,e,N);
        newPow(c, m, e, N);
       }
    } while (lineCount == 3 );
    mpz_clear( N );
    mpz_clear( e );
    mpz_clear( m );

}

void stage1() {
  // fill in this function with solution
  	mpz_t N, e, m, c;
    int lineCount = 0;
    mpz_inits(N,e,m,c,NULL);
    do{
      lineCount = gmp_scanf( "%Zx\n%Zx\n%Zx", N, e, m );
       if(lineCount == 3){
        newPow(c, m, e, N);
        gmp_printf( "%Zx\n", c );
       }
    } while (lineCount == 3 );
    mpz_clear( N );
    mpz_clear( e );
    mpz_clear( m );

}

/*
Perform stage 2:

- read each 9-tuple of N, d, p, q, d_p, d_q, i_p, i_q and c from stdin,
- compute the RSA decryption m,
- then write the plaintext m to stdout.
*/

void stage2() {
    mpz_t N, d, p, q, d_p, d_q, i_p, i_q, c, m, u, temp1, temp2;
    int lineCount = 0;
    mpz_inits(N,d,p,q,d_p,d_q,i_p,i_q,c,m,u,temp1, temp2, NULL);
    do{
      lineCount = gmp_scanf( "%Zx\n%Zx\n%Zx\n%Zx\n%Zx\n%Zx\n%Zx\n%Zx\n%Zx",N,d, p, q, d_p, d_q, i_p, i_q, c);
      if(lineCount == 9){
        CRT(N, d, p, q, d_p, d_q, i_p, i_q, c, m, u, temp1, temp2);
        gmp_printf( "%Zx\n", m );
      }
    }while (lineCount == 9);
    mpz_clear( N );mpz_clear( d );mpz_clear( p );
    mpz_clear( q );mpz_clear( d_p );mpz_clear( d_q );
    mpz_clear( i_p );mpz_clear( i_q );mpz_clear( c );
    mpz_clear( m );
}

/*
Perform stage 3:

- read each 5-tuple of p, q, g, h and m from stdin,
- compute the ElGamal encryption c = (c_1,c_2),
- then write the ciphertext c to stdout.
*/






void stage3() {

  // fill in this function with solution
    mpz_t p, q, g, h, m, c1, c2, k, seed;
    int lineCount = 0;

    int seedVal = time(NULL);
    gmp_randstate_t randState;

    mpz_inits(p,q,g,h,m,c1,c2,k, seed, NULL);


    mpz_set_ui(seed, seedVal);
    gmp_randinit_default(randState);
    do{

      lineCount  =gmp_scanf( "%Zx\n%Zx\n%Zx\n%Zx\n%Zx",  p,q,g,h,m );
      gmp_randseed (randState, seed);
      mpz_urandomm(k, randState, q);
      if(lineCount == 5){
        newPow(c1, g, k, p);
        newPow(c2, h, k, p);
        mpz_mul(c2, c2, m);
        mpz_mod(c2, c2, p);
        gmp_printf( "%Zx\n", c1 );      
        gmp_printf( "%Zx\n", c2 );
      }

    }while(lineCount == 5);
      mpz_clear( p );mpz_clear( q );mpz_clear( g );
      mpz_clear( h );mpz_clear( m );mpz_clear( c1 );
      mpz_clear( c2 ); mpz_clear( k );mpz_clear( seed );



}

/*
Perform stage 4:

- read each 5-tuple of p, q, g, x and c = (c_1,c_2) from stdin,
- compute the ElGamal decryption m,
- then write the plaintext m to stdout.
*/

void stage4() {

  // fill in this function with solution
    mpz_t p, q, g, h, m, c1, c2;
    int lineCount = 0;
    mpz_inits(p,q,g,h,m,c1,c2, NULL);
    do{
      lineCount  =gmp_scanf( "%Zx\n%Zx\n%Zx\n%Zx\n%Zx\n%Zx",  p,q,g,h,c1,c2 );
      if(lineCount == 6){
        mpz_sub(m, q, h);
        newPow(m, c1, m, p);
        mpz_mul(m, m, c2);   
        mpz_mod(m, m, p);   
        gmp_printf( "%Zx\n", m );
      }
    }while(lineCount == 6);
    mpz_clear( p );mpz_clear( q );mpz_clear( g );
    mpz_clear( h );mpz_clear( m );mpz_clear( c1 );
    mpz_clear( c2 );
}

/*
The main function acts as a driver for the assignment by simply invoking
the correct function for the requested stage.
*/

int main( int argc, char* argv[] ) {
  if     ( !strcmp( argv[ 1 ], "stage1" ) ) {
    stage1();
  }
  else if( !strcmp( argv[ 1 ], "stage2" ) ) {
    stage2();
  }
  else if( !strcmp( argv[ 1 ], "stage3" ) ) {
    stage3();
  }
  else if( !strcmp( argv[ 1 ], "stage4" ) ) {
    stage4();
  } 
  else if( !strcmp( argv[ 1 ], "test" ) ) {
    test();
  }

  return 0;
}
