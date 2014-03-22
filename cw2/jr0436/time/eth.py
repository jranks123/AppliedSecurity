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


def montExp(N, x, y):
	pSquared = calcPSquared(N)
	omega = calcOmega(N)
	t = montMul(N, 1, pSquared, omega)
	xHat = montMul(N, x, pSquared, omega)
	print t
	print xHat
	sizeOfY = math.ceil(math.log(y, 2))
	binY = bin(y).lstrip("0b")
	binY =  format(int(binY, 2), '0'+ str(int(sizeOfY)) + 'b')
	count = 0
	for i in range(0, int(sizeOfY)):
		t = montMul(N, t,t, omega)
		#print binY[i]
		if binY[i] == '1':
			t = montMul(N, t, xHat, omega)
	t = montMul(N, t, 1, omega)
	#print count
	return t



def attack(A) :
	with open(A) as thefile:
	    lines = thefile.readlines()  

	n = lines[0]
	e = lines[1]
	t,r = interact(e)




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
  x = 14777912434722484012795150747433197744767136897217162407762927865455435847145735686915331827545464755796807234471871479852466934757357239598392518626677060360692000372538879569563006291417336461597266487127830346581372131687317440322423575802518877104255558126974558449677855388857647750426674157655378030063
  y = 82066906503981187431857367827616517547742026992296675269535396889324683244050948742697807615775012316882267807115314093017053946984947287322227475300115586985710753917221939474324908096704688427033412500308916929487658423364451145032970068348791689894471753550784886649253371303609895809157663585850520032959 
  omega = 3821265123607851245 
  N = 90294311424406673228338297200726006944631753630845809306519637227101667889745832477888085683126958592769170203506611034167697397910397535705315263098112563532540303944988972364693194890784306135883557032253343377823721157298262490305418829735604172267015074712472931277122629288704655390257429427388301857563 
  result = montExp(N, x, y)
  print('result = %d' %result)