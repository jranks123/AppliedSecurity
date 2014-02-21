#ifndef __MODMUL_H
#define __MODMUL_H

#include  <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#include <string.h>

#include    <gmp.h>

#endif

void montRed(mpz_t result, mpz_t x, mpz_t omega, mpz_t N, mpz_t b){
    mpz_t r, u, Nshift;
    mpz_inits(r, Nshift, u, NULL);
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
    mpz_t omega, N, e, m, b, c, result;
    int lineCount = 0;
    mpz_inits(N, omega, e,m,c, b, result, NULL);
    mpz_setbit(b,64);
    do{
      lineCount = gmp_scanf( "%Zx\n%Zx\n%Zx", N, e, m );
       if(lineCount == 3){
        mpz_set_ui(m, 421);
        mpz_set_ui(N, 667);
        calculateOmega(omega, N, b);
        montRed(result, m, omega, N, b);
        gmp_printf("T = %Zd\n", result);
        newPow(result, m, m, N);

       // gmp_printf("%Zx", c);
       }
    } while (lineCount == 3 );
    mpz_clear( N );
    mpz_clear( e );
    mpz_clear( m );

}