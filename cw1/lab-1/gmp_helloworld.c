#include "gmp_helloworld.h"

 #define max(a,b) \
   ({ __typeof__ (a) _a = (a); \
       __typeof__ (b) _b = (b); \
     _a > _b ? _a : _b; })
     
int main( int argc, char* argv[] ) {
	mpz_t r, x, y;

	mpz_init( r );
	mpz_init( x );
	mpz_init( y );
	int i;
	gmp_scanf( "%Zd",  x );
	gmp_scanf( "%Zd",  y );
	size_t nx = mpz_size( x );
	size_t ny = mpz_size( y );
	int l_r = max(nx,ny)+1;
	mp_limb_t tx[ nx+1 ];
	mp_limb_t ty[ ny+1 ];
	mpz_export( tx, NULL, -1, sizeof( mp_limb_t ), -1, 0, x );
	mpz_export( ty, NULL, -1, sizeof( mp_limb_t ), -1, 0, y );
  
  
  
  
	mp_limb_t rt[l_r];

	rt[ l_r - 1 ] = mpn_add(rt, tx, nx, ty, ny);   //NOTE must make sure x is bigger or equal to y, if there is a carry it only informs me, doesnt give me whole answer


	for (i = 0; i<l_r; i++){
		gmp_printf( "Total =  %llu\n", rt[i] );
	}

	//mpz_import( r, sizeof(mp_limb_t), -1, sizeof(mp_limb_t), -1, 0, rt );
	//gmp_printf( "Total = %Zd\n", r );
	mpz_clear( r );
	mpz_clear( x );
	mpz_clear( y );

	return 0;
}

/*#include "gmp_dissect_export.h"

int main( int argc, char* argv[] ) {
  mpz_t x;

  mpz_init( x );

  gmp_scanf( "%Zd", x );

  size_t n = mpz_size( x );
  printf("Limb bits = %d\n", GMP_LIMB_BITS);
  mp_limb_t t[ n ];

  mpz_export( t, NULL, -1, sizeof( mp_limb_t ), -1, 0, x );

  for( int i = 0; i < n; i++ ) {
    if( i != 0 ) {
      printf( "+" );
    }

    printf( "%llu*(2^(64))^(%d)", t[ i ], i );
  }

  printf( "\n" );

  mpz_clear( x );

  return 0;
}*/
