import sys, subprocess, math, os, random




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
	for i in range (0, int(limbCount)):
		limbs.append(x & mask)
		x = x >> 64
	return limbs



def getLimbI(x, i):
	mask = 18446744073709551615
	x = x >> 64*i
	r = x&mask
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
	t = 1
	r = 2*getLN(N)*64
	for i in range(0, int(r)):
		t = (t +t)%N
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
	x0 = getLimbI(x, 0)
	for i in range(0, int(getLN(N))):
		u = ((getLimbI(r,0) + getLimbI(y,i)*x0) * omega)%b
		r = (r + (getLimbI(y,i)*x) + u*N)/b
		if r >= N:
			r = r-N
	return r


def montMulRedCheck(N, x, y, omega):
	r = 0
	b = 2**64
	x0 = getLimbI(x, 0)
	for i in range(0, int(getLN(N))):
		u = ((getLimbI(r,0) + getLimbI(y,i)*x0) * omega)%b
		r = (r + (getLimbI(y,i)*x) + u*N)/b
		red = False
		if r >= N:
			red = True
			r = r-N
	return r, red



def montExp(N, x, binY, sizeOfY, pSquared, omega, t, xHat, tList1, tList0):

	#print binY
	#for i in range(0, sizeOfY):
		#if (i == sizeOfY-1):
			#print 'old binY %s' %binY	
			#binY = binY[:-1] + '1'
			#print 'new 1 binY %s' %binY	
	tTemp = montMul(N, t,t, omega)
	tTemp = montMul(N, tTemp, xHat, omega)
	tTemp, red1 = montMulRedCheck(N, tTemp,tTemp, omega)
	tList1.append(tTemp)


	tTemp = montMul(N, t,t, omega)
	tTemp, red0 = montMulRedCheck(N, tTemp,tTemp, omega)
	tList0.append(tTemp)

	
			

	#t = montMul(N, t, 1, omega)
	return t, red1, red0, tList1, tList0



def getAverage(l):
	if len(l) == 0:
		return 0
	av = 0
	for i in range (0, len(l)):
		av += l[i]
	return av/len(l)

def attack(A) :
	with open(A) as thefile:
	    lines = thefile.readlines()  

	n = lines[0]
	e = lines[1]

	nP = int(n, 16)
	eP = int(e, 16)

	pSquared = calcPSquared(nP)
	omega = calcOmega(nP)
	t = montMul(nP, 1, pSquared, omega)


	ctimeList = [] 
	tList = []
	xList = []
	for i in range (0, 10000):
		c = '%128x' % random.randrange(16**128)
		w ,r = interact(c)
		ctimeList.append([c, w])
		xHat = montMul(nP, int(c, 16), pSquared, omega)
		tTemp = montMul(nP, t,t, omega)
		tTemp = montMul(nP, tTemp, xHat, omega)
		xList.append(xHat)
		tList.append(tTemp)




	K = '1'
	kSize = 1
	for i in range(0, 64):
		kSize += 1
		b1 = []
		b2 = []
		b3 = []
		b4 = []
		tList1 = []
		tList0 = []	
		for i in range (0, 10000):
			c = int(ctimeList[i][0], 16)
			time = int(ctimeList[i][1], 16) 
			xHat = xList[i]
			t = tList[i]
			Ktemp = K
			t, red1, red0, tList1, tList0 = montExp(nP, c, Ktemp, kSize, pSquared, omega, t, xHat, tList1, tList0)
			if(red1 == True):
				b1.append(time)
			else:
				b2.append(time)
			if(red0 == True):
				b3.append(time)
			else:
				b4.append(time)
		chance1 = getAverage(b1) - getAverage(b2)
		chance0 = getAverage(b3) - getAverage(b4)
		if(chance0 > chance1):
			K = K + '0'
			print 'Differnce was %d' %chance0
			tList = tList0
		else:
			K = K + '1'
			print 'Difference was %d'%chance1
			tList = tList1
		print 'K = %s' %K





if ( __name__ == "__main__" ) :
  # Produce a sub-process representing the attack target.
  target = subprocess.Popen( args   = sys.argv[ 1 ],
                             stdout = subprocess.PIPE, 
                             stdin  = subprocess.PIPE )

  # Construct handles to attack target standard input and output.
  target_out = target.stdout
  target_in  = target.stdin

  attack(sys.argv[2])
  #result = montExp(N, x, y)
  #print('result = %d' %result)


