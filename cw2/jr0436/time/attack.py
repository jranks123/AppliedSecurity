import sys, subprocess, math, os, random, platform
from Crypto.Util import number
  



def ceildiv(a, b):
	(c,d) = divmod(a,b)
	if(d != 0):
		return a//b + 1
	else:
		return a//b







def montExpOld(N, x, y, pSquared, p, omega):
	t = newMontMul(N, 1, pSquared, p, omega)
	xHat = newMontMul(N, x, pSquared, p, omega)
#	print t
#	print xHat
	sizeOfY = math.ceil(math.log(y, 2))
	binY = bin(y).lstrip("0b")
	binY =  format(int(binY, 2), '0'+ str(int(sizeOfY)) + 'b')
	count = 0
	for i in range(0, int(sizeOfY)):
		t = newMontMul(N, t,t, p, omega)
		#print binY[i]
		if binY[i] == '1':
			t = newMontMul(N, t, xHat, p, omega)
	t = newMontMul(N, t, 1, p, omega)
	#print count
	return t



def getLN(x, base):
	return math.ceil(math.log(x, 2**base))



def interact( G ) :
	#print(G)
	# Send      G      to   attack target.
	target_in.write( "%s\n" % ( G ) ) ; target_in.flush()

	# Receive ( t, r ) from attack target.
	t =  target_out.readline().strip() 
	r = target_out.readline().strip() 
	return(t,r)



def calcPSquared(N, base):
	t = 1
	r = 2*getLN(N, base)*base
	for i in range(0, int(r)):
		t = (t +t)%N
	return t

def calcP(N, base):
	b = 2**base
	i = 1
	while b**i < N:
		i += 1
	r = b**i
	return r


def newCalcOmega(N, p):
	return (( -(number.inverse(N, p))) % p)


def calcOmega(N, base):
	t = 1
	b = pow(2,base)
	for i in range(0, base-1):
		t = (t*t*N)%b
	t = (-t)%b
	return t
#def montgomery():

def newMontMul(N, x,y, p, omega):
	r = x*y
	r = (r + ((r*omega%p)*N))/p
	if r >= N:
		r = r-N
	return r

def newMontMulRedCheck(N, x,y, p, omega):
	r = x*y
	r = (r + ((r*omega%p)*N))/p
	red = False
	if r >= N:
		red = True
		r = r-N
	return r, red





def montExp(N, x, binY, sizeOfY, pSquared, omega, t, xHat, tList1, tList0, p, newOmega):
	tTemp = newMontMul(N, t,t, p, newOmega)
	t1 = newMontMul(N, tTemp, xHat, p, newOmega)
	tList1.append(t1)
	t1, red1 = newMontMulRedCheck(N, t1,t1, p, newOmega)

	tList0.append(tTemp)
	t0, red0 = newMontMulRedCheck(N, tTemp,tTemp, p, newOmega)
	return t, red1, red0, tList1, tList0



def getAverage(l):
	if len(l) == 0:
		return 0
	av = 0
	for i in range (0, len(l)):
		av += l[i]
	return av/len(l)

def attack(A, numberOfSamples) :
	with open(A) as thefile:
	    lines = thefile.readlines()  

	base = int(platform.architecture()[0][:-3])
	n = lines[0]
	e = lines[1]


	nP = int(n, 16)
	eP = int(e, 16)
	lN = getLN(nP, base)
	b = 2**base


	pSquared = calcPSquared(nP, base)
	p = calcP(nP, base)
	newOmega = newCalcOmega(nP, p)
	
	omega = calcOmega(nP, base)
	t = newMontMul(nP, 1, pSquared, p, newOmega)


	


	ctimeList = [] 
	tList = []
	xList = []
	for i in range (0, numberOfSamples):
		c = random.randrange(16**128)		
		cHex = '%128x' % c
		w ,r = interact(cHex)
		ctimeList.append([c, w])
		xHat = newMontMul(nP, c, pSquared, p, newOmega)
		tTemp = newMontMul(nP, t,t, p, newOmega)
		tTemp = newMontMul(nP, tTemp, xHat, p, newOmega)
		xList.append(xHat)
		tList.append(tTemp)

	#	print 'xHat 1 = %d' %xHat
		#print 'tTemp 1 = %d' %tTemp



	found = False
	K = '1'
	kSize = 1
	while found == False:
		#print ('NEW NUMBER\n')
		kSize += 1
		b1 = []
		b2 = []
		b3 = []
		b4 = []
		tList1 = []
		tList0 = []	
		for i in range (0, numberOfSamples):
			c = ctimeList[i][0]
			time = int(ctimeList[i][1])
			xHat = xList[i]
			t = tList[i]
			Ktemp = K
			t, red1, red0, tList1, tList0 = montExp(nP, c, Ktemp, kSize, pSquared, omega, t, xHat, tList1, tList0, p, newOmega)
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
			print 'Difference was %d' %chance0
			tList = tList0
			greater = chance0
		else:
			K = K + '1'
			print 'Difference was %d'%chance1
			tList = tList1
			greater = chance1
		print 'K = %s' %K

		number = 2314234
		kMaybe1 = int(K[:-1]+'1', 2)
		if montExpOld(nP, montExpOld(nP, number, eP, pSquared, p, newOmega), kMaybe1, pSquared, p, newOmega) == number:
			print 'the key is %s' %K[:-1]+'1'
			found = True
			exit()
		kMaybe0 = int(K[:-1]+'0', 2)
		if montExpOld(nP, montExpOld(nP, number, eP, pSquared, p, newOmega), kMaybe0, pSquared, p, newOmega) == number:
			print 'the key is %s' %K[:-1]+'0'
			found = True
			exit()	
		if greater< 3:
			print 'failed with %d numberOfSamples, trying again with %s' %(numberOfSamples, numberOfSamples + 1000)
			attack(A, numberOfSamples+1000)
		



if ( __name__ == "__main__" ) :
  # Produce a sub-process representing the attack target.
  target = subprocess.Popen( args   = sys.argv[ 1 ],
                             stdout = subprocess.PIPE, 
                             stdin  = subprocess.PIPE )

  # Construct handles to attack target standard input and output.

  target_out = target.stdout
  target_in  = target.stdin
  numberOfSamples = 6000
  attack(sys.argv[2], numberOfSamples)
  #result = montExp(N, x, y)
  #print('result = %d' %result)

