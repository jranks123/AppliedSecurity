#include <Python.h>
#include <openssl/aes.h>


#define listFromPyToArray(array, list) { \                    
  for (int i = 0; i < 16; i++) \                         
    array[i] = PyInt_AS_LONG(PyList_GET_ITEM(list, i)); \
}

#define keyFromPy(k, eqResults) {                     \
  k[ 2] = PyInt_AS_LONG( PyList_GET_ITEM(eqResults[2], 0));  \
  k[ 3] = PyInt_AS_LONG( PyList_GET_ITEM(eqResults[3], 0));  \
  k[ 4] = PyInt_AS_LONG(PyTuple_GET_ITEM(eqResults[1], 0));  \
  k[ 5] = PyInt_AS_LONG( PyList_GET_ITEM(eqResults[2], 1));  \
  k[ 6] = PyInt_AS_LONG( PyList_GET_ITEM(eqResults[3], 1));  \
  k[ 7] = PyInt_AS_LONG(PyTuple_GET_ITEM(eqResults[0], 0));  \
  k[ 8] = PyInt_AS_LONG( PyList_GET_ITEM(eqResults[2], 2));  \
  k[ 9] = PyInt_AS_LONG( PyList_GET_ITEM(eqResults[3], 2));  \
  k[10] = PyInt_AS_LONG(PyTuple_GET_ITEM(eqResults[0], 1));  \
  k[11] = PyInt_AS_LONG(PyTuple_GET_ITEM(eqResults[1], 1));  \
  k[12] = PyInt_AS_LONG( PyList_GET_ITEM(eqResults[3], 3));  \
  k[13] = PyInt_AS_LONG(PyTuple_GET_ITEM(eqResults[0], 2));  \
  k[14] = PyInt_AS_LONG(PyTuple_GET_ITEM(eqResults[1], 2));  \
  k[15] = PyInt_AS_LONG( PyList_GET_ITEM(eqResults[2], 3));  \
}


const uint8_t sbox[] = {
  0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
  0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
  0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
  0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
  0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
  0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
  0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
  0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
  0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
  0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
  0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
  0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
  0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
  0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
  0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
  0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16 };

const uint8_t rsbox[] = {
  0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
  0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
  0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
  0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
  0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
  0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
  0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
  0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
  0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
  0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
  0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
  0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
  0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
  0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
  0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
  0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D };

const uint8_t aes_round_constant[] = { 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36 };

uint8_t gf_mulx(uint8_t a) {
  if ((a & 0x80) == 0x80) return 0x1B ^ (a << 1);
  else return (a << 1);
}

uint8_t gf_mul(uint8_t a, uint8_t b) {
  uint16_t  t = 0;

  for (int i = 7; i >= 0; i--) {
    t = gf_mulx(t);
    if ((b >> i) & 1) t ^= a;
  }

  return t;
}

int isCorrectKey(uint8_t *k, uint8_t *m, uint8_t *c) {
  uint8_t t[ 16 ];

  AES_KEY rk;

  AES_set_encrypt_key( k, 128, &rk );
  AES_encrypt( m, t, &rk );  

  if( !memcmp( t, c, 16 * sizeof( uint8_t ) ) ) return 1;
  else return 0;
}


uint8_t gf_inv(uint8_t a) {
  uint8_t t_0;
  uint8_t t_1;
  t_0 = gf_mul(a, a) ;    
  t_1 = gf_mul(t_0, a);    
  t_0 = gf_mul(t_0, t_0); 
  t_1 = gf_mul(t_1, t_0);  
  t_0 = gf_mul(t_0, t_0); 
  t_0 = gf_mul(t_1, t_0);  
  t_0 = gf_mul(t_0, t_0); 
  t_0 = gf_mul(t_0, t_0);  
  t_1 = gf_mul(t_1, t_0); 
  t_0 = gf_mul(t_0, t_1);  
  t_0 = gf_mul(t_0, t_0); 

  return t_0;
 }



void keyReverseStep(uint8_t *k, uint8_t *r, int roundNumber) {
  k[15] =                   r[11]  ^ r[15];
  k[14] =                   r[10]  ^ r[14];
  k[13] =                   r[ 9]  ^ r[13];
  k[12] =                   r[ 8]  ^ r[12];

  k[11] =                   r[ 7]  ^ r[11];
  k[10] =                   r[ 6]  ^ r[10];
  k[ 9] =                   r[ 5]  ^ r[ 9];
  k[ 8] =                   r[ 4]  ^ r[ 8];

  k[ 7] =                   r[ 3]  ^ r[ 7];
  k[ 6] =                   r[ 2]  ^ r[ 6];
  k[ 5] =                   r[ 1]  ^ r[ 5];
  k[ 4] =                   r[ 0]  ^ r[ 4];

  uint8_t rc = aes_round_constant[roundNumber];

  k[ 3] =      sbox[k[12]] ^ r[ 3];
  k[ 2] =      sbox[k[15]] ^ r[ 2];
  k[ 1] =      sbox[k[14]] ^ r[ 1];
  k[ 0] = rc ^ sbox[k[13]] ^ r[ 0];
}

void keyReverse(uint8_t *k, uint8_t *rk10) {
  uint8_t k_temp[16] = { 0 };
  // copy rk10 into k_temp
  for (int i = 0; i < 16; i++)
    k_temp[i] = rk10[i];
  for (int i = 9; i > -1; i--) // loop from 10 down to 1 (incl.)
    keyReverseStep(k_temp, k_temp, i);
  // copy k_temp into k
  for (int i = 0; i < 16; i++)
    k[i] = k_temp[i];
}

// main body of step2. Returns 1 if found key, 0 otherwise
int getKey(uint8_t *kArray, uint8_t *mArray, uint8_t *xArray, uint8_t *xPrimeArray, PyObject *eqResults, PyObject *k0Potentials, PyObject *k1Potentials) {
  PyObject *eqLists[4];
  PyObject *k0s;
  PyObject *k1s;
   PyObject *kKey = PyTuple_New(3);
  PyObject* ka ;
  PyObject* kb;
  PyObject* kc;
  PyObject *q[4];
  Py_ssize_t k0size;
    Py_ssize_t k1size;
  uint8_t h10 = aes_round_constant[9];
  uint8_t gf2 = gf_inv(2);
  uint8_t gf3 = gf_inv(3);
  Py_ssize_t eqLengths[4] = { 0 };
  PyObject *kLists[2];
  Py_ssize_t qLengths[4] = { 0 };
  unsigned long long count = 0, total = 0;
  int candidateCount = 0;
  uint8_t potentialKey[16] = { 0 };
  uint8_t f, fPrime, threeF, twoF;
  for (int i = 0; i < 4; i++) {
      eqLists[i] = PyList_GET_ITEM(eqResults, i); 
      eqLengths[i] = PyList_GET_SIZE(eqLists[i]);
  }

 

  for(int i = 0; i < eqLengths[0]; i++){
    q[0] = PyList_GET_ITEM(eqLists[0], i);
    kArray[13] = PyInt_AS_LONG( PyList_GET_ITEM(q[0], 0));
    kArray[10] = PyInt_AS_LONG( PyList_GET_ITEM(q[0], 1));
    kArray[7] = PyInt_AS_LONG( PyList_GET_ITEM(q[0], 2));

   // printf("%d\n",kArray[10] );
  	for(int j = 0; j < eqLengths[1]; j++){
      q[1] = PyList_GET_ITEM(eqLists[1], j);
      kArray[4] = PyInt_AS_LONG( PyList_GET_ITEM(q[1], 0));
      kArray[14] = PyInt_AS_LONG( PyList_GET_ITEM(q[1], 1));
      kArray[11] = PyInt_AS_LONG( PyList_GET_ITEM(q[1], 2));

  		for(int k = 0; k < eqLengths[2]; k++){
        q[2] = PyList_GET_ITEM(eqLists[2], k);
        kArray[8] = PyInt_AS_LONG( PyList_GET_ITEM(q[2], 0));
        kArray[5] = PyInt_AS_LONG( PyList_GET_ITEM(q[2], 1));
        kArray[2] = PyInt_AS_LONG( PyList_GET_ITEM(q[2], 2));
        kArray[15] = PyInt_AS_LONG( PyList_GET_ITEM(q[2], 3));
  			for(int l = 0; l < eqLengths[3]; l++){
          count ++;
          if(count%10000000 == 0){
            printf("Completed %d rounds\n", count );
          }
          q[3] = PyList_GET_ITEM(eqLists[3], l);
          kArray[12] = PyInt_AS_LONG( PyList_GET_ITEM(q[3], 0));
          kArray[9] = PyInt_AS_LONG( PyList_GET_ITEM(q[3], 1));
          kArray[6] = PyInt_AS_LONG( PyList_GET_ITEM(q[3], 2));
          kArray[3] = PyInt_AS_LONG( PyList_GET_ITEM(q[3], 3));
           f = rsbox[gf_mul((rsbox[xArray[12] ^ kArray[12]] ^ (kArray[12] ^ kArray[8])), 9) \
                    ^ gf_mul((rsbox[xArray[9] ^ kArray[9]] ^ (kArray[9] ^ kArray[13])),14) \
                    ^gf_mul((rsbox[xArray[6] ^ kArray[6]] ^ (kArray[14]^ kArray[10])),11) \
                    ^gf_mul((rsbox[xArray[3] ^ kArray[3]] ^ (kArray[15] ^ kArray[11])), 13)] \
                    ^rsbox[gf_mul((rsbox[xPrimeArray[12] ^ kArray[12]] ^ (kArray[12] ^ kArray[8])), 9) \
                    ^ gf_mul((rsbox[xPrimeArray[9] ^ kArray[9]] ^ (kArray[9] ^ kArray[13])),14) \
                    ^gf_mul((rsbox[xPrimeArray[6] ^ kArray[6]] ^ (kArray[14] ^ kArray[10])),11) \
                    ^gf_mul((rsbox[xPrimeArray[3] ^ kArray[3]] ^ (kArray[15] ^ kArray[11])), 13)] ;

          if((rsbox[gf_mul((rsbox[xArray[8] ^ kArray[8]] ^ (kArray[8] ^ kArray[4])), 13) \
                    ^ gf_mul((rsbox[xArray[5] ^ kArray[5]] ^ (kArray[9] ^ kArray[5])),9) \
                    ^gf_mul((rsbox[xArray[2] ^ kArray[2]] ^ (kArray[10]^ kArray[6])),14) \
                    ^gf_mul((rsbox[xArray[15] ^ kArray[15]] ^ (kArray[11] ^ kArray[7])), 11)] \
                    ^rsbox[gf_mul((rsbox[xPrimeArray[8] ^ kArray[8]] ^ (kArray[8] ^ kArray[4])), 13) \
                    ^ gf_mul((rsbox[xPrimeArray[5] ^ kArray[5]] ^ (kArray[9] ^ kArray[5])),9) \
                    ^gf_mul((rsbox[xPrimeArray[2] ^ kArray[2]] ^ (kArray[10]^ kArray[6])),14) \
                    ^gf_mul((rsbox[xPrimeArray[15] ^ kArray[15]] ^ (kArray[11] ^ kArray[7])), 11)]) == f){


              
              ka = Py_BuildValue("i", kArray[13]);
              kb= Py_BuildValue("i", kArray[10]);
              kc = Py_BuildValue("i", kArray[7]);
              PyTuple_SetItem(kKey, 0, ka);
              PyTuple_SetItem(kKey, 1, kb);
              PyTuple_SetItem(kKey, 2, kc);
              k0s = PyDict_GetItem(k0Potentials, kKey);
              ka = Py_BuildValue("i", kArray[4]);
              kb= Py_BuildValue("i", kArray[14]);
              kc = Py_BuildValue("i", kArray[11]);
              PyTuple_SetItem(kKey, 0, ka);
              PyTuple_SetItem(kKey, 1, kb);
              PyTuple_SetItem(kKey, 2, kc);
              k1s = PyDict_GetItem(k1Potentials, kKey);
              k0size = PyList_GET_SIZE(k0s);
              k1size = PyList_GET_SIZE(k1s);
            //  PyObject* objectsRepresentation = PyObject_Repr(k0s);
             // const char* s = PyString_AsString(objectsRepresentation);
             // printf("%d\n", PyInt_AS_LONG( PyList_GET_ITEM(k0s, 0)));
             // printf("%s\n", s);
             // printf("%d\n", PyList_GET_SIZE(k0s););
             // exit(0);
              for(int l = 0; l < k0size; l++){
                for(int m = 0; m < k1size; m++){
                   kArray[0] = PyInt_AS_LONG( PyList_GET_ITEM(k0s, l));
                   kArray[1] = PyInt_AS_LONG( PyList_GET_ITEM(k1s, m));
                    
               
                  if(  gf_mul(rsbox[gf_mul( ( rsbox[xArray[0] ^ kArray[0]] ^ kArray[0] ^ sbox[kArray[13] ^ kArray[9] ] ^ h10), 14) \
                      ^ gf_mul((rsbox[ xArray[13] ^ kArray[13]]^(kArray[1] ^ sbox[kArray[14] ^ kArray[10]])),11) \
                      ^ gf_mul((rsbox[ xArray[10] ^ kArray[10]] ^ (kArray[2] ^ sbox[kArray[15] ^ kArray[11]])),13) \
                      ^ gf_mul((rsbox[ xArray[7] ^ kArray[7]] ^ (kArray[3] ^ sbox[kArray[12] ^ kArray[8]])), 9)] \
                      ^ rsbox[gf_mul( ( rsbox[xPrimeArray[0] ^ kArray[0]] ^ kArray[0] ^ sbox[kArray[13] ^ kArray[9] ] ^ h10), 14) \
                      ^ gf_mul((rsbox[ xPrimeArray[13] ^ kArray[13]]^(kArray[1] ^ sbox[kArray[14] ^ kArray[10]])),11) \
                      ^ gf_mul((rsbox[ xPrimeArray[10] ^ kArray[10]] ^ (kArray[2] ^ sbox[kArray[15] ^ kArray[11]])),13) \
                      ^ gf_mul((rsbox[ xPrimeArray[7] ^ kArray[7]] ^ (kArray[3] ^ sbox[kArray[12] ^ kArray[8]])), 9)], gf2) ==f ){
                      if(gf_mul(rsbox[gf_mul((rsbox[xArray[4] ^ kArray[4]] ^ (kArray[4] ^ kArray[0])), 11) \
                            ^ gf_mul((rsbox[xArray[1] ^ kArray[1]] ^ (kArray[5] ^ kArray[1])),13) \
                            ^gf_mul((rsbox[xArray[14] ^ kArray[14]] ^ (kArray[6]^ kArray[2])),9) \
                            ^gf_mul((rsbox[xArray[11] ^ kArray[11]] ^ (kArray[7] ^ kArray[3])), 14)] \
                            ^rsbox[gf_mul((rsbox[xPrimeArray[4] ^ kArray[4]] ^ (kArray[4] ^ kArray[0])), 11) \
                            ^ gf_mul((rsbox[xPrimeArray[1] ^ kArray[1]] ^ (kArray[5] ^ kArray[1])),13) \
                            ^gf_mul((rsbox[xPrimeArray[14] ^ kArray[14]] ^ (kArray[6]^ kArray[2])),9) \
                            ^gf_mul((rsbox[xPrimeArray[11] ^ kArray[11]] ^ (kArray[7] ^ kArray[3])), 14)], gf3) == f){

                              keyReverse(potentialKey, kArray);
                             
                            if (isCorrectKey(potentialKey, mArray, xArray)) {
                                printf("Found key after checking %llu combinations\n", count);

                                 for(int c = 0; c < 16; c++){
                                  printf("%d,",potentialKey[c] );
                                }
                                // copy candidate key array to output array
                                return 1;
                              }
                            
                            
                              
                             

                      }



                  }



                }
            }
              
        }
            }



  			}
  		}
  	}
  


  // SOME LONG LOOP HERE THAT BRUTEFORCES THE STEP 2 EQUATIONS
  // if reached this point, then key hasn't been found, so return 0*/
  return 0;
}




static PyObject *stage2(PyObject *self, PyObject *args) {

  PyObject *mList, *xList, *xPrimeList, *eqResults, *k0Potentials, *k1Potentials;

  uint8_t kArray[16] = { 0 };
  uint8_t mArray[16] = { 0 };
  uint8_t xArray[16] = { 0 };
  uint8_t xPrimeArray[16] = { 0 };



  if (!PyArg_ParseTuple(args, "OOOOOO", &mList, &xList, &xPrimeList, &eqResults, &k0Potentials, &k1Potentials))
    return NULL;

  listFromPyToArray(xArray, xList);
  listFromPyToArray(xPrimeArray, xPrimeList);
  listFromPyToArray(mArray, mList);


  int kIsFound = getKey(kArray, mArray, xArray, xPrimeArray, eqResults, k0Potentials, k1Potentials);


  if (!kIsFound) Py_RETURN_NONE;

  PyObject * kList = PyList_New(16);

  // copy keyArray to keyList and return back to Python
  for (int i = 0; i < 16; i++) {
    PyObject *kByte= PyInt_FromLong(kArray[i]);
    if (!kByte) {
      Py_DECREF(kList);
      return NULL;
    }  
    PyList_SET_ITEM(kList, i, kByte); // reference to byte stolen, so no need to DECREF
  	
  }

  return kList;
}


// method table
static PyMethodDef stage2_methods[] = {
    { "stage2", stage2, METH_VARARGS, "Exectute stage 2" },
    { NULL, NULL, 0, NULL }           /* sentinel */
};


PyMODINIT_FUNC initstage2() {
  Py_InitModule("stage2", stage2_methods);
};


