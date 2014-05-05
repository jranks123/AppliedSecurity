
#	for k1 in range (0, 256):
#		find the delta
#		add the delta to s set
#		at hash[delta] add k1 = [0,3] #
#
#	for k2 in range (0,256)#
#		at hash add k2 = [4.6.756.]
#
#	s1&s2&s3&s4
#
#	list of deltas#
#
#	hashtable[65] =  

	#	a = hex(int(x[1], 16)^k)[2:].zfill(2)
    #	b = hex(int(xPrime[1], 16)^k)[2:].zfill(2)
	#	c = rsbox[int(a[0:1], 16)*16 + int(a[1:2], 16)]
	#	d = rsbox[int(b[0:1], 16)*16 + int(b[1:2], 16)]
		#print rsbox
		#print c
		#print d
	#	print  int(xor_strings('{0:08b}'.format(c), '{0:08b}'.format(d)).encode("hex"),2)
#		print c ^ d

import sys, subprocess, math, os, random, platform
import struct, Crypto.Cipher.AES as AES

from collections import defaultdict

def aes(k, m):
  k = struct.pack( 16 * "B", *k )
  m = struct.pack( 16 * "B", *m )


  t = AES.new( k ).encrypt( m )

  return struct.unpack(16 * "B", t)

def aes2():
  k = [ 0x2B, 0x7E, 0x15, 0x16, 0x28, 0xAE, 0xD2, 0xA6, \
        0xAB, 0xF7, 0x15, 0x88, 0x09, 0xCF, 0x4F, 0x3C ]
  m = [ 0x32, 0x43, 0xF6, 0xA8, 0x88, 0x5A, 0x30, 0x8D, \
        0x31, 0x31, 0x98, 0xA2, 0xE0, 0x37, 0x07, 0x34 ]
  c = [ 0x39, 0x25, 0x84, 0x1D, 0x02, 0xDC, 0x09, 0xFB, \
        0xDC, 0x11, 0x85, 0x97, 0x19, 0x6A, 0x0B, 0x32 ]

  k = struct.pack( 16 * "B", *k )
  m = struct.pack( 16 * "B", *m )
  c = struct.pack( 16 * "B", *c )

  t = AES.new( k ).encrypt( m )

  if( t == c ) :
    print "AES.Enc( k, m ) == " + str(struct.unpack(16 * "B", c))
  else :
    print "AES.Enc( k, m ) != c"

rsbox = [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3,
            0x9e, 0x81, 0xf3, 0xd7, 0xfb , 0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f,
            0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb , 0x54,
            0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b,
            0x42, 0xfa, 0xc3, 0x4e , 0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24,
            0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25 , 0x72, 0xf8,
            0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d,
            0x65, 0xb6, 0x92 , 0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda,
            0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84 , 0x90, 0xd8, 0xab,
            0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3,
            0x45, 0x06 , 0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1,
            0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b , 0x3a, 0x91, 0x11, 0x41,
            0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6,
            0x73 , 0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9,
            0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e , 0x47, 0xf1, 0x1a, 0x71, 0x1d,
            0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b ,
            0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0,
            0xfe, 0x78, 0xcd, 0x5a, 0xf4 , 0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07,
            0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f , 0x60,
            0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f,
            0x93, 0xc9, 0x9c, 0xef , 0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5,
            0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61 , 0x17, 0x2b,
            0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55,
            0x21, 0x0c, 0x7d]

sbox =  [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67,
        0x2b, 0xfe, 0xd7, 0xab, 0x76, 0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59,
        0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0, 0xb7,
        0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1,
        0x71, 0xd8, 0x31, 0x15, 0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05,
        0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75, 0x09, 0x83,
        0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29,
        0xe3, 0x2f, 0x84, 0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b,
        0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf, 0xd0, 0xef, 0xaa,
        0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c,
        0x9f, 0xa8, 0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc,
        0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 0xcd, 0x0c, 0x13, 0xec,
        0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19,
        0x73, 0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee,
        0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb, 0xe0, 0x32, 0x3a, 0x0a, 0x49,
        0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
        0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4,
        0xea, 0x65, 0x7a, 0xae, 0x08, 0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6,
        0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a, 0x70,
        0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9,
        0x86, 0xc1, 0x1d, 0x9e, 0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e,
        0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf, 0x8c, 0xa1,
        0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0,
        0x54, 0xbb, 0x16]



def gf_mul(a, b):
    p = 0
    for counter in range(8):
        if b & 1: 
        	p ^= a
        hi_bit_set = a & 0x80
        a <<= 1
        a &= 0xFF
        if hi_bit_set:
            a ^= 0x1b
        b >>= 1
    return p

def gf_inv(a) :
  t_0 = gf_mul(a, a)      # a^2
  t_1 = gf_mul(t_0, a)    # a^3
  t_0 = gf_mul(t_0, t_0)  # a^4
  t_1 = gf_mul(t_1, t_0)  # a^7
  t_0 = gf_mul(t_0, t_0)  # a^8
  t_0 = gf_mul(t_1, t_0)  # a^15
  t_0 = gf_mul(t_0, t_0)  # a^30
  t_0 = gf_mul(t_0, t_0)  # a^60
  t_1 = gf_mul(t_1, t_0)  # a^67
  t_0 = gf_mul(t_0, t_1)  # a^127
  t_0 = gf_mul(t_0, t_0)  # a^254

  return t_0
  
  
  
def convert(int_value):
   encoded = format(int_value, 'x')

   length = len(encoded)
   encoded = encoded.zfill(2)
   return encoded




def interact( parameters, m ) :
	# Send      G      to   attack target.
	target_in.write( "%s\n" % ( parameters) ) ; target_in.flush()
	target_in.write( "%s\n" % ( m) ) ; target_in.flush()
	# Receive ( t) from attack target.
	t = ( target_out.readline().strip() )
	return t



def generateHex() :
	c = random.randrange(16**32)		
	cHex = '%32x' % c
	return cHex

def generateHex2() :
	cArray = []
	for i in range (0, 16):
		cHex = os.urandom(1).encode('hex')
		cArray.append(cHex)
	return cArray

def xor_strings(xs, ys):
    return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(xs, ys))


def generateHypotheses(delta, hypotheses, d) :
	for i in d[delta]['k1'] :
		for j in d[delta]['k2'] :
			for k in d[delta]['k3'] :
				for l in d[delta]['k4'] :
					hypotheses.append([i,j,k,l])

	return hypotheses

def generateK0hyp (delta, hypotheses, d, k0Potentials, k1Potentials) :

	for i in d[delta]['k1'] :
		for j in d[delta]['k2'] :
			for k in d[delta]['k3'] :
				for l in d[delta]['k4'] :
					dupeHypo = False
					for n in range (0, len(hypotheses)):
						if hypotheses[n] == [k,l]:
							dupeHypo = True
					if not dupeHypo:
						hypotheses.append([k,l])
					temp = str(k).zfill(3)+str(l).zfill(3)
					if temp not in k0Potentials.keys():
						k0Potentials[temp] = []
					if temp not in k1Potentials.keys():
						k1Potentials[temp] = []
					dupe0 = False
					for p in k0Potentials[temp]:
						if i == p:
							dupe0 = True
					if not dupe0:
						k0Potentials[temp].append(i)
					dupe1 = False
					for w in k1Potentials[temp]:
						if j == w:
							dupe1 = True
					if not dupe1:
						k1Potentials[temp].append(j)
					
	return (hypotheses, k0Potentials, k1Potentials)


def generateK1hyp (delta, hypotheses, d) :
	k1Potentials = {}
	for i in d[delta]['k1'] :
		for j in d[delta]['k2'] :
			for k in d[delta]['k3'] :
				for l in d[delta]['k4'] :
					hypotheses.append([i,k,l])
					temp = str(i)+str(k)+str(l)
					if temp not in k1Potentials.keys():
						k1Potentials[temp] = []
					k1Potentials[temp].append(j)
	return (hypotheses, k1Potentials)

def calcQuad(x, xPrime, k1, gf1, k2, gf2, k3, gf3,  k4, gf4) :
	k1 = k1-1
	k2 = k2-1
	k3 = k3-1
	k4 = k4-1
	s1 = set()  #store deltas
	s2 = set()
	s3 = set()
	s4 = set()

	d1 = {}



	for k in range (0, 256):
		delta = gf_mul(rsbox[int(x[k1],16) ^ k] ^ rsbox[int(xPrime[k1], 16) ^ k],gf_inv(gf1))
		s1.add(delta)
		if delta not in d1.keys():
			d1[delta] = {'k1' : [], 'k2' : [], 'k3' : [], 'k4' : []}
		d1[delta]['k1'].append(k)


	for k in range (0, 256):
		delta = gf_mul(rsbox[int(x[k2],16) ^ k] ^ rsbox[int(xPrime[k2], 16) ^ k],gf_inv(gf2))
		s2.add(delta)
		if delta not in d1.keys():
			d1[delta] = {'k1' : [], 'k2' : [], 'k3' : [], 'k4' : []}
		d1[delta]['k2'].append(k)

	for k in range (0, 256):
		delta = gf_mul(rsbox[int(x[k3],16) ^ k] ^ rsbox[int(xPrime[k3], 16) ^ k],gf_inv(gf3))
		s3.add(delta)
		if delta not in d1.keys():
			d1[delta] = {'k1' : [], 'k2' : [], 'k3' : [], 'k4' : []}
		d1[delta]['k3'].append(k)

	for k in range (0, 256):
		delta = gf_mul(rsbox[int(x[k4],16) ^ k] ^ rsbox[int(xPrime[k4], 16) ^ k],gf_inv(gf4))
		s4.add(delta)
		if delta not in d1.keys():
			d1[delta] = {'k1' : [], 'k2' : [], 'k3' : [], 'k4' : []}
		d1[delta]['k4'].append(k)


	hypotheses = []
	validDeltas = s1&s2&s3&s4
	if (k1 != 0 ):
		for i in validDeltas:
			hypotheses = generateHypotheses(i, hypotheses, d1)

		return hypotheses

	elif k1 == 0:
		k0Potentials = {}
		k1Potentials = {}
		for i in validDeltas:
			(hypotheses, k0Potentials, k1Potentials) = generateK0hyp(i, hypotheses, d1, k0Potentials, k1Potentials)
		return (hypotheses, k0Potentials, k1Potentials)


	#elif k2 == 1:

	#	k1Potentials = {}
	#	for i in validDeltas:
	#		(hypotheses, k1Potentials) = generateK1hyp(i, hypotheses, d1)
	#	return (hypotheses, k1Potentials)





def findMatch(a, b):
	for i in a:
		for j in b:
			if i == j:
				return i
	return 0

		

aes_round_constant = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]



def keyReverseStep(r, roundNumber) :
  k = [0] * 16
 
  k[ 4] =                   r[ 0]  ^ r[ 4]
  k[ 5] =                   r[ 1]  ^ r[ 5]
  k[ 6] =                   r[ 2]  ^ r[ 6]
  k[ 7] =                   r[ 3]  ^ r[ 7]
 
  k[ 8] =                   r[ 4]  ^ r[ 8]
  k[ 9] =                   r[ 5]  ^ r[ 9]
  k[10] =                   r[ 6]  ^ r[10]
  k[11] =                   r[ 7]  ^ r[11]
 
  k[12] =                   r[ 8]  ^ r[12]
  k[13] =                   r[ 9]  ^ r[13]
  k[14] =                   r[10]  ^ r[14]
  k[15] =                   r[11]  ^ r[15]
 
  rc = aes_round_constant[roundNumber]
 
  k[ 0] = rc ^ sbox[k[13]] ^ r[ 0]
  k[ 1] =      sbox[k[14]] ^ r[ 1]
  k[ 2] =      sbox[k[15]] ^ r[ 2]
  k[ 3] =      sbox[k[12]] ^ r[ 3]

  return k
 

def keyReverse(k) :
  k_temp = k[:] 
  for i in reversed(xrange(0, 10)):
    k_temp = keyReverseStep(k_temp, i)
  return k_temp
	
	
def cheat(xArray, xPrimeArray, xPrimeArray2):
	firstFault1 = calcQuad(xArray, xPrimeArray, 1, 2, 14,1, 11, 1, 8, 3)
	secondFault1 = calcQuad(xArray, xPrimeArray2, 1, 2, 14,1, 11, 1, 8, 3)

	firstFault2 = calcQuad(xArray, xPrimeArray, 5, 1, 2, 1, 15, 3, 12, 2)
	secondFault2 = calcQuad(xArray, xPrimeArray2, 5, 1, 2, 1, 15, 3, 12, 2)

	firstFault3 = calcQuad(xArray, xPrimeArray, 9, 1, 6,3, 3, 2, 16, 1)
	secondFault3 = calcQuad(xArray, xPrimeArray2, 9, 1, 6,3, 3, 2, 16, 1)

	firstFault4 = calcQuad(xArray, xPrimeArray, 13, 3, 10,2, 7, 1, 4, 1)
	secondFault4 = calcQuad(xArray, xPrimeArray2, 13, 3, 10,2, 7, 1, 4, 1)

	
	quad1 = findMatch(firstFault1,secondFault1)
	quad2 = findMatch(firstFault2,secondFault2)
	quad3 = findMatch(firstFault3,secondFault3)
	quad4 = findMatch(firstFault4,secondFault4)

	k1 = quad1[0]
	k14 = quad1[1]
	k11 = quad1[2]
	k8 = quad1[3]

	k5 = quad2[0]
	k2 = quad2[1]
	k15 = quad2[2]
	k12 = quad2[3]

	k9 = quad3[0]
	k6 = quad3[1]
	k3 = quad3[2]
	k16 = quad3[3]

	k13 = quad4[0]
	k10 = quad4[1]
	k7 = quad4[2]
	k4 = quad4[3]
	
	result = k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11, k12, k13, k14, k15, k16

	r = ""
	for i in result:
	 	r = r + str(hex(i).lstrip("0x").zfill(2))
	print "actual K = " + r
	return result

	
	
def attack() :
	r = '8'
	f = '1'
	p = '0'
	i = '0'
	j = '0'
	tuple = r+','+f+','+p+','+i+','+j
	#m = generateHex()
	m = "50d1d99af6d169ea9a439eb9965c72e7"
	m2 = (int(m[0:2], 16),int(m[2:4], 16),int(m[4:6], 16),int(m[6:8], 16),int(m[8:10], 16),int(m[10:12], 16),int(m[12:14], 16)\
		,int(m[14:16], 16), int(m[16:18], 16),int(m[18:20], 16),int(m[20:22], 16),int(m[22:24], 16),int(m[24:26], 16),int(m[26:28], 16),\
		int(m[28:30], 16),int(m[30:32], 16) )
	x = interact("", m)

	numX = (int(x[0:2], 16),int(x[2:4], 16),int(x[4:6], 16),int(x[6:8], 16),int(x[8:10], 16),int(x[10:12], 16),int(x[12:14], 16)\
		,int(x[14:16], 16), int(x[16:18], 16),int(x[18:20], 16),int(x[20:22], 16),int(x[22:24], 16),int(x[24:26], 16),int(x[26:28], 16),\
		int(x[28:30], 16),int(x[30:32], 16) )
	xPrime = interact(tuple, m)
	xPrime2 = interact(tuple, m)
	#x = "359A5B18E6132847AD6D16B0FEB45E53"#
	#xPrime = "71C86574B48DA0D2C874D730715205B0"
	xArray = []
	xPrimeArray = []
	xPrimeArray2 = []
	for i in range(0, 16):
		xArray.append(x[2*i:2*i+2])
	for i            in range(0, 16):
		xPrimeArray.append(xPrime[2*i:2*i+2])
	for i in range(0, 16):
		xPrimeArray2.append(xPrime2[2*i:2*i+2])

	k0Potentials = {}
	k1Potentials = {}
	#actualK = cheat(xArray, xPrimeArray, xPrimeArray2)
	(firstFault1 , k0Potentials, k1Potentials) = calcQuad(xArray, xPrimeArray, 1, 2, 14,1, 11, 1, 8, 3)
	firstFault2 = calcQuad(xArray, xPrimeArray, 5, 1, 2, 1, 15, 3, 12, 2)
	firstFault3 = calcQuad(xArray, xPrimeArray, 9, 1, 6,3, 3, 2, 16, 1)
	firstFault4 = calcQuad(xArray, xPrimeArray, 13, 3, 10,2, 7, 1, 4, 1)

	xNum = []
	xPrimeNum = []
	for i in xArray:
		xNum.append(int(i, 16))
	for i in xPrimeArray:
		xPrimeNum.append(int(i, 16))

	x1 = xNum[0]
	x2 = xNum[1]
	x3 = xNum[2]
	x4 = xNum[3]
	x5 = xNum[4]
	x6 = xNum[5]
	x7 = xNum[6]
	x8 = xNum[7]
	x9 = xNum[8]
	x10 = xNum[9]
	x11= xNum[10]
	x12 = xNum[11]
	x13 = xNum[12]
	x14 = xNum[13]
	x15 = xNum[14]
	x16 = xNum[15]

	x1P = xPrimeNum[0]
	x2P = xPrimeNum[1]
	x3P = xPrimeNum[2]
	x4P = xPrimeNum[3]
	x5P = xPrimeNum[4]
	x6P = xPrimeNum[5]
	x7P = xPrimeNum[6]
	x8P = xPrimeNum[7]
	x9P = xPrimeNum[8]
	x10P = xPrimeNum[9]
	x11P = xPrimeNum[10]
	x12P = xPrimeNum[11]
	x13P = xPrimeNum[12]
	x14P = xPrimeNum[13]
	x15P = xPrimeNum[14]
	x16P = xPrimeNum[15]
	print len(firstFault1)
	for i in range (0, len(firstFault1)):
		for j in range (0, len(firstFault2)):
			for k in range (0, len(firstFault3)):
				for l in range (0, len(firstFault4)):
					K = firstFault1[i]+firstFault2[j]+firstFault3[k]+firstFault4[l]

					#Equation 1
					#k1 = K[0]
					#k2 = K[1]
					k3 = K[0]
					k4 = K[1]
					k5 = K[2]
					k6 = K[3]
					k7 = K[4]
					k8 = K[5]
					k9 = K[6]
					k10 = K[7]
					k11= K[8]
					k12 = K[9]
					k13 = K[10]
					k14= K[11]
					k15 = K[12]
					k16 = K[13]
					h10 = aes_round_constant[9]


	



					
					f = rsbox[gf_mul((rsbox[x13 ^ k13] ^ (k13 ^ k9)), 9) \
					^ gf_mul((rsbox[x10 ^ k10] ^ (k10 ^ k14)),14) \
					^gf_mul((rsbox[x7 ^ k7] ^ (k15 ^ k11)),11) \
					^gf_mul((rsbox[x4 ^ k4] ^ (k16 ^ k12)), 13)] \
					^rsbox[gf_mul((rsbox[x13P ^ k13] ^ (k13 ^ k9)), 9) \
					^ gf_mul((rsbox[x10P ^ k10] ^ (k10 ^ k14)),14) \
					^gf_mul((rsbox[x7P ^ k7] ^ (k15 ^ k11)),11) \
					^gf_mul((rsbox[x4P ^ k4] ^ (k16 ^ k12)), 13)] 
						
					if rsbox[gf_mul((rsbox[x9 ^ k9] ^ (k9 ^ k5)), 13) \
					^ gf_mul((rsbox[x6 ^ k6] ^ (k10 ^ k6)),9) \
					^gf_mul((rsbox[x3 ^ k3] ^ (k11 ^ k7)),14) \
					^gf_mul((rsbox[x16 ^ k16] ^ (k12 ^ k8)), 11)] \
					^rsbox[gf_mul((rsbox[x9P ^ k9] ^ (k9 ^ k5)), 13) \
					^ gf_mul((rsbox[x6P ^ k6] ^ (k10 ^ k6)),9) \
					^gf_mul((rsbox[x3P ^ k3] ^ (k11 ^ k7)),14) \
					^gf_mul((rsbox[x16P ^ k16] ^ (k12 ^ k8)), 11)]  == f :
						for n in range (0, len(k0Potentials)):
							for m in range(0, len(k1Potentials)):
								kTwoToFour =str(k3).zfill(3) + str(k4).zfill(3)
								for o in k0Potentials[kTwoToFour]:
									for p in k1Potentials[kTwoToFour]:
										k1 = o
										k2 = p
										if gf_mul(rsbox[gf_mul( ( rsbox[x1 ^ k1] ^ k1 ^ sbox[k14 ^ k10] ^ h10), 14) \
										^ gf_mul((rsbox[ x14 ^ k14]^(k2 ^ sbox[k15 ^ k11])),11) \
										^ gf_mul((rsbox[ x11^ k11] ^ (k3 ^ sbox[k16 ^ k12])),13) \
										^ gf_mul((rsbox[ x8 ^ k8] ^ (k4 ^ sbox[k13 ^ k9])), 9)] \
										^ rsbox[gf_mul((rsbox[x1P ^ k1] ^ k1 ^ sbox[k14 ^ k10] ^ h10), 14) \
										^ gf_mul((rsbox[ x14P ^ k14]^(k2 ^ sbox[k15 ^ k11])),11) \
										^ gf_mul((rsbox[ x11P ^ k11] ^ (k3 ^ sbox[k16 ^ k12])),13) \
										^ gf_mul((rsbox[ x8P ^ k8] ^ (k4 ^ sbox[k13 ^ k9])), 9)], gf_inv(2)) == f:
											if gf_mul(rsbox[gf_mul((rsbox[x5 ^ k5] ^ (k5 ^ k1)), 11) \
											^ gf_mul((rsbox[x2 ^ k2] ^ (k6 ^ k2)),13) \
											^gf_mul((rsbox[x15 ^ k15] ^ (k7 ^ k3)),9) \
											^gf_mul((rsbox[x12 ^ k12] ^ (k8 ^ k4)), 14)] \
											^rsbox[gf_mul((rsbox[x5P ^ k5] ^ (k5 ^ k1)), 11) \
											^ gf_mul((rsbox[x2P ^ k2] ^ (k6 ^ k2)),13) \
											^gf_mul((rsbox[x15P ^ k15] ^ (k7 ^ k3)),9) \
											^gf_mul((rsbox[x12P ^ k12] ^ (k8 ^ k4)), 14)], gf_inv(3)) == f :
												if aes(	keyReverse(K), m2) == numX:
													print("success")
													exit()
												else:
													print ("fail")

					#print aes(K, m2)
	
	#result = aes(actualK, m2)
	#print result
	#r = ""
	#for i in result:
	# 	r = r + str(hex(i).lstrip("0x").zfill(2))
	#print "possib X = " + r






if ( __name__ == "__main__" ) :
  # Produce a sub-process representing the attack target.
  target = subprocess.Popen( args   = sys.argv[ 1 ],
                             stdout = subprocess.PIPE, 
                             stdin  = subprocess.PIPE )

  # Construct handles to attack target standard input and output.


  target_out = target.stdout
  target_in  = target.stdin
  attack()
