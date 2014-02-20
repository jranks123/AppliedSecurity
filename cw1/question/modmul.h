#ifndef __MODMUL_H
#define __MODMUL_H

#include  <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#include <string.h>

#include    <gmp.h>

#endif

void CRT(mpz_t N,mpz_t d,mpz_t p,mpz_t q,mpz_t d_p,mpz_t d_q,mpz_t i_p,mpz_t i_q,mpz_t c,mpz_t m,mpz_t u,mpz_t temp1,mpz_t temp2){
     newPow(temp1, c, d_q,q);
     newPow(temp2, c, d_p,p);
    //mpz_powm(temp1, c, d_q, q);
  //  mpz_powm(temp2, c, d_p, p);
    

    mpz_sub(u, temp1, temp2);
    mpz_mul(u, u, i_p);
    mpz_mod(u,u,q);

    mpz_mul(m, p, u);
    mpz_add(m, m, temp2);
    mpz_mod(m,m,N);

}
