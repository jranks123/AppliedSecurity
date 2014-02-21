#include "modmul.h"
#include <gmp.h>
#include "math.h"

#define DEBUG 1
#if DEBUG
  #define SHOWERROR() printf("line %d in function %s in file %s\n", __LINE__, __FUNCTION__, __FILE__);
#else
  #define SHOWERROR(); 
#endif

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
void CRT(mpz_t N,mpz_t d,mpz_t p,mpz_t q,mpz_t d_p,mpz_t d_q,mpz_t i_p,mpz_t i_q,mpz_t c,mpz_t m,mpz_t u,mpz_t temp1,mpz_t temp2){
    mpz_t(cHold);
    mpz_init(cHold);
    mpz_mod(cHold, c, q);
    newPow(temp1, cHold, d_q,q);
    mpz_mod(cHold, c, p);
    newPow(temp2, cHold, d_p,p);
    //mpz_powm(temp1, c, d_q, q);
    //  mpz_powm(temp2, c, d_p, p);


    mpz_sub(u, temp1, temp2);
    mpz_mul(u, u, i_p);
    mpz_mod(u,u,q);

    mpz_mul(m, p, u);
    mpz_add(m, m, temp2);
    mpz_mod(m,m,N);

}

void calculateT(int tSize, mpz_t* T, mpz_t x, mpz_t N, mpz_t omega, mpz_t u2, mpz_t temp, mpz_t b, mpz_t r, unsigned long long t, unsigned long long nModB){
    int i = 0;
    int k = 0;
    mpz_t xSquared;
    mpz_inits(T[0], xSquared, NULL);
    mpz_set(T[0], x);
    ZnModMul(xSquared, x, x, N, omega, u2, temp, b, r, t, nModB); 
    //mpz_mul(xSquared, x, x);
    //mpz_mod(xSquared, xSquared, N);  
    for(i = 1; i < tSize; i++){
      mpz_init(T[i]);
      ZnModMul(T[i], T[i-1], xSquared, N, omega, u2, temp, b, r, t, nModB);
      //mpz_mul(T[i], T[i-1], xSquared);
      //mpz_mod(T[i], T[i], N);  
    }
    mpz_clear(xSquared);
}

void newPow(mpz_t t, mpz_t x, mpz_t y, mpz_t N){
  int k = 4;
  double m = pow(2,k);
  size_t tSize = round(m/2);
  unsigned long long t2;
  mpz_t T[tSize], xBar, omega, pSqared, one, u2, temp, b, r;
  mpz_inits(t, pSqared, xBar, omega, one, u2, temp, b, r, NULL);
  mpz_setbit(b, 64);
  mpz_set_ui(pSqared, 1);
  mpz_set_ui(one, 1);
  calculatePSquared(pSqared, N);
  calculateOmega(omega,N);
  unsigned long long nModB = mpz_getlimbn(omega, 0);
 // mpz_mod(x, x, N);
  ZnModMul(xBar, x, pSqared, N, omega, u2, temp, b, r, t2, nModB);
  ZnModMul(t, one, pSqared , N, omega, u2, temp, b, r, t2, nModB);
  calculateT(tSize, T, xBar, N, omega, u2, temp, b, r, t2, nModB);
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
         ZnModMul(t, t, t, N, omega, u2, temp, b, r, t2, nModB);
      }

        if(u != 0){
            size_t q = (u-1)/2;

            ZnModMul(t, t, T[q], N, omega, u2, temp, b, r, t2, nModB);
        }
      i = l-1;
    }

   for(i = 0; i < tSize; i++){
      mpz_clear( T[i] );
  }
  ZnModMul(t, t, one, N, omega, u2, temp, b, r, t, nModB);
   mpz_clear(xBar);
   mpz_clear(omega);
   mpz_clear(pSqared);
   mpz_clear(one);
}

void calculateOmega(mpz_t x, mpz_t N){
//  gmp_printf("%Zd\n", N);
    mpz_t zero, b;
    mpz_inits(zero, b, NULL);
    int w = 64;
    mpz_set_ui(b,0);
    mpz_setbit(b, 64);
    unsigned long long t = 1;
    size_t nx = mpz_size( N );  //COULD OPTIMISE AS SOME OF THESE CALCS ARE DONE IN CALCULATEPSQUARED
    mp_limb_t tx[ nx ];
    mpz_export(tx, NULL, -1, sizeof( mp_limb_t ), -1, 0, N );
    unsigned long long nModB = tx[0];
    int i;
    for(i = 1; i < w; i++){
      t = t*t*nModB;
    }
    mpz_set_ui (x,t);
    mpz_sub(x, b, x);
}

/*void calculateOmega2(mpz_t x, mpz_t N){
//  gmp_printf("%Zd\n", N);
    mpz_set_ui(x, 1);
    mpz_t b, temp;
    mpz_t zero;
    mpz_init(zero);
    mpz_inits(b, temp, NULL);
    mpz_set_ui(b,0);
    mpz_setbit(b, 64);
    //gmp_printf("%Zd\n", b);
    int i;
    for(i = 0; i < 64; i++){
      //gmp_printf("%Zd\n", x);
      mpz_mul(x, x, x);
      mpz_mod(temp, N, b);
     // gmp_printf("temp = %Zd\n", temp);
      mpz_mul(x, x, temp);
     // gmp_printf("x after mul= %Zd\n", x);
      mpz_mod(x, x, b);
      //gmp_printf("x after mod = %Zd\n", x);
    }
    mpz_sub(x, zero, x);
    mpz_mod(x, x, b);
}*/



void calculatePSquared(mpz_t t, mpz_t N){
    int i;
    int w = 64;
    size_t nx = mpz_size( N ); 
    for(i = 0; i < w*nx*2; i++){
        mpz_add(t, t, t);
        mpz_mod(t, t, N);
    }
}

void calculateP(mpz_t t, mpz_t N){
    mpz_setbit(t, mpz_size( N )*64);
}

void ZnModMul(mpz_t result, mpz_t x, mpz_t y, mpz_t N, mpz_t omega, mpz_t u, mpz_t temp, mpz_t b, mpz_t r, unsigned long long t, unsigned long long nModB){
  int i;
  size_t Tx = mpz_size( N );
  mpz_set_ui(r, 0);
  unsigned long long x0;
 // x0  = mpz_getlimbn(x,0);
  x0  = x->_mp_d[0];
  unsigned long long yI;
  size_t ySize = mpz_size(y);
  for(i = 0; i < Tx; i++){
   // yI = mpz_getlimbn(y,i);
    yI = i<ySize? y->_mp_d[i]: 0;
   // printf("%d\n", yI);
    t = (r->_mp_d[0]+(yI*x0))*nModB;
    mpz_mul_ui(temp, x,  yI);
    mpz_mul_ui(u, N, t);
    mpz_add(u, temp, u);
    mpz_add(r, r, u);
    mpz_fdiv_q_2exp(r, r, 64); 

  }
    if(mpz_cmp(r, N)>=0){
      mpz_sub(r, r, N);

   }
   mpz_set(result, r);


}



void montRed(mpz_t result, mpz_t x, mpz_t omega, mpz_t N){
    mpz_t r, b, u, Nshift;
    mpz_inits(r, b, Nshift, u, NULL);
    mpz_setbit(b, 64);
    mpz_set(r, x);
    int i;
    size_t nx = mpz_size( N ); 
    unsigned long long x0 = mpz_getlimbn(x,0);
    unsigned long long omega0 = mpz_getlimbn(omega,0);
    unsigned long long uInt;
    for( i = 0; i < nx; i++){
      uInt = mpz_getlimbn(r, i)*omega0; 
      mpz_mul_2exp(Nshift, N, 64*i); 
      mpz_mul_ui(u, Nshift, uInt); 
      mpz_add(r, r, u); 
    }
    mpz_fdiv_q_2exp(r, r, 64*nx); 
      if(mpz_cmp(r, N)>=0){
      mpz_sub(r, r, N);

   }
   mpz_set(result, r);
}



void test() {
  // fill in this function with solution
    mpz_t omega, N, e, m, c, result;
    int lineCount = 0;
    mpz_inits(N, omega, e,m,c, result, NULL);

    do{
      lineCount = gmp_scanf( "%Zx\n%Zx\n%Zx", N, e, m );
       if(lineCount == 3){
        mpz_set_ui(m, 421);
        mpz_set_ui(N, 667);
        calculateOmega(omega, N);
        montRed(result, m, omega, N);
        gmp_printf("T = %Zd\n", result);
        newPow(result, m, m, N);

       // gmp_printf("%Zx", c);
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

    unsigned long long randVal;
    FILE *fp;
    fp = fopen("/dev/urandom", "r");
    int output = fread(&randVal, 8, 1, fp);
    fclose(fp);

    if(!output)
    {
          printf("Error reading values");
          return;
    }





    gmp_randstate_t randState;

    mpz_inits(p,q,g,h,m,c1,c2,k, seed, NULL);


    mpz_set_ui(seed, randVal);
    gmp_randinit_default(randState);
    do{

      lineCount  =gmp_scanf( "%Zx\n%Zx\n%Zx\n%Zx\n%Zx",  p,q,g,h,m );
      gmp_randseed (randState, seed);
      mpz_urandomm(k, randState, q);
      mpz_set_ui(k, 1);
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
    mpz_t p, q, g, h, m, c1, c2, hold1, hold2;
    int lineCount = 0;
    mpz_inits(p,q,g,h,m,c1,c2, hold1, hold2, NULL);
    do{
      lineCount  =gmp_scanf( "%Zx\n%Zx\n%Zx\n%Zx\n%Zx\n%Zx", p,q,g,h,c1,c2 );
      if(lineCount == 6){
        mpz_sub(hold1, q, h);
        newPow(hold2, c1, hold1, p);
       // mpz_powm(m, c1, m, p);
        mpz_mul(m, hold2, c2);   
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
