import sys, subprocess, math




def ceildiv(a, b):
	(c,d) = divmod(a,b)
	if(d != 0):
		return a//b + 1
	else:
		return a//b

#def getLimbCount(x):#
#	N = int('80955794bdb73369df4b8c1dbb3ffb5965b3494a787e369b4a80606d6ece157b3333950204abf9003ed9f601837b7d29d8e0a5e3f6ace7339ee1864bdae9c3ef92fe137c5ebc94768e6f3c82a6496131c1a64cfebff05aefd55c0749e4315de0599d9b3d2bdb530739035d01cb772fd05153be495252c98e1572ac725ab2531b', 16)

#	b = len(str(bin(x)).lstrip("0b"))
#	print(math.ceil(math.log(N, 2**64)))
#	return ceildiv(b,64)



def intToLimbs(x):
	mask = 18446744073709551615
	limbCount = getLN(x)
	limbs = []
	print(limbCount)
	for i in range (0, int(limbCount)):
		limbs.append(x & mask)
		x = x >> 64
	return limbs



def getLimbI(x, i):
	mask = 18446744073709551615
	x = x >> 64*i
	r = x&mask
	print r
	return r





def getLN(x):
	return math.ceil(math.log(x, 2**64))



def interact( G ) :
	#print(G)
	# Send      G      to   attack target.
	target_in.write( "%s\n" % ( G ) ) ; target_in.flush()

	# Receive ( t, r ) from attack target.
	t =  target_out.readline().strip() 
	r = target_out.readline().strip() 
	return(t,r)



def calcPSquared(N):
	N = int('80955794bdb73369df4b8c1dbb3ffb5965b3494a787e369b4a80606d6ece157b3333950204abf9003ed9f601837b7d29d8e0a5e3f6ace7339ee1864bdae9c3ef92fe137c5ebc94768e6f3c82a6496131c1a64cfebff05aefd55c0749e4315de0599d9b3d2bdb530739035d01cb772fd05153be495252c98e1572ac725ab2531b', 16)
	t = 1
	r = 2*getLN(N)*64
	for i in range(0, int(r)):
		t = (t +t)%N
		print 't = %s' %t
	return t


def calcOmega(N):
	t = 1
	w = 64
	b = pow(2,64)
	for i in range(0, w-1):
		t = (t*t*N)%b
	t = (-t)%b
	return t
#def montgomery():


def montMul(N, x, y, omega):
	r = 0
	b = 2**64
	y = intToLimbs(y)
	x0 = getLimbI(x, 0)
	for i in range(0, int(getLN(N))):
		u = ((getLimbI(r,0) + y[i]*x0) * omega)%b
		r = (r + (y[i]*x) + u*N)/b
		if r >= N:
			r = r-N
	return r


def montExp(N, omega, x, y):
	pSquared = calcPSquared(N)
	omega = calcOmega(N)
	t = montMul(N, 1, pSquared, omega)
	x = montMul(N, x, pSquared, omega)
	binY = bin(y)
	sizeOfY = math.ceil(math.log(y, 2))
	for i in range(int(sizeOfY), 0):
		t = montMul(N, t,t)



def attack(A) :
	with open(A) as thefile:
	    lines = thefile.readlines()  

	n = lines[0]
	e = lines[1]
	t,r = interact(e)
	print t, r



if ( __name__ == "__main__" ) :
  # Produce a sub-process representing the attack target.
  target = subprocess.Popen( args   = sys.argv[ 1 ],
                             stdout = subprocess.PIPE, 
                             stdin  = subprocess.PIPE )

  # Construct handles to attack target standard input and output.
  target_out = target.stdout
  target_in  = target.stdin

  #calcPSquared(3)
  #intToLimbs(int('80955794bdb73369df4b8c1dbb3ffb5965b3494a787e369b4a80606d6ece157b3333950204abf9003ed9f601837b7d29d8e0a5e3f6ace7339ee1864bdae9c3ef92fe137c5ebc94768e6f3c82a6496131c1a64cfebff05aefd55c0749e4315de0599d9b3d2bdb530739035d01cb772fd05153be495252c98e1572ac725ab2531b', 16))
  #getLimbI(int('80955794bdb73369df4b8c1dbb3ffb5965b3494a787e369b4a80606d6ece157b3333950204abf9003ed9f601837b7d29d8e0a5e3f6ace7339ee1864bdae9c3ef92fe137c5ebc94768e6f3c82a6496131c1a64cfebff05aefd55c0749e4315de0599d9b3d2bdb530739035d01cb772fd05153be495252c98e1572ac725ab2531b', 16), 4)

  #intToLimbs(5467474675435687563958359357927867249578234572347474)
  #intToLimbs(3)
  # Execute a function representing the attacker.
  #attack(sys.argv[2])