import sys, subprocess, math
from hashlib import sha1




def ceildiv(a, b):
	(c,d) = divmod(a,b)
	if(d != 0):
		return a//b + 1
	else:
		return a//b



def interact( G ) :
	#print(G)
	# Send      G      to   attack target.
	target_in.write( "%s\n" % ( G ) ) ; target_in.flush()

	# Receive ( t, r ) from attack target.
	t = int( target_out.readline().strip() )



	return ( t )

def I2OSP(m, k):
	if(m > pow(256, k)):
		print('integer too long')
		return
	m = ('%X' %m)
	m = m.zfill(k)
	return m



def MGF(mgfSeed, maskLen):
	hLen = 40
	hashFunction = sha1
	if(maskLen > pow(2, 32)*maskLen*2):
		print('mask too long')
		return
	t = ""
	counter = 0
	while counter < ceildiv(maskLen, hLen):
		C = I2OSP(counter, 8)
		mgC = str(mgfSeed) + str(C)
		t += hashFunction(mgC.decode("hex")).hexdigest()
		counter = counter+1
	return t[:maskLen]


def unpad(m,k):
	k = k*2
	hLen = 40
	octSize = 2
	EM = I2OSP(m, k)
  	maskedSeed = EM[2:42]
  	maskedDB = EM[42:]
  	seedMask = MGF(maskedDB, hLen)
  	seed = hex(int(seedMask, 16) ^ int(maskedSeed, 16)).rstrip("L").lstrip("0x") or "0"
  	dbMask = MGF(seed, k-hLen-2)
 	DB = hex(int(maskedDB, 16) ^ int(dbMask, 16)).rstrip("L").lstrip("0x") or "0" 	
  	print(DB)



  	



def attack(A) :
	with open(A) as thefile:
	    lines = thefile.readlines()  

	n = lines[0]
	e = lines[1]
	c = lines[2]


	nP = int(n, 16)
	eP = int(e, 16)
	cP = int(c, 16)



	k = math.ceil(math.log(int(n, 16), 256))
	B = pow(2, 8*(int(k)-1))
	

	#STAGE1
	f1 = 1
	result = 0
	while result != 1:
		f1 = f1*2
		r = (pow(f1, eP, nP)*cP)%nP
		r = hex(int(r)).rstrip("L").lstrip("0x") or "0"
		result = (interact(r.zfill(256)))

	print "f1 = %d" %f1

	#STAGE2
	f2 = int(math.floor(((nP+B)//B))*(f1/2))
	print "f2 before = " + str(f2)
	while(result == 1):
		f2New = (pow(f2, eP, nP)*cP)%nP
		f2Hex = hex(int(f2New)).rstrip("L").lstrip("0x") or "0"
		result = (interact(f2Hex.zfill(256)))
		if result == 1 :
			f2 = f2+(f1/2)
		print "f2 in = " + str(f2)
	print "f2 = " + str(f2)

	#stage3
	mMin = ceildiv(nP, f2)
	mMax = (nP + B)//f2
	print"F2*(MAX - mIN) - B = %d" %(f2*(mMax-mMin)-B)
	while(math.fabs(mMax-mMin)>0):

		fTmp = (2*B)//(mMax-mMin)
		i = (fTmp*mMin) // nP
		f3 = ceildiv((i*nP), mMin)
		f3Hex= (pow(f3, eP, nP)*cP)%nP
		f3Hex = hex(int(f3Hex)).rstrip("L").lstrip("0x") or "0"
		result = (interact(f3Hex.zfill(256)))
		if result == 1:
			mMin = ceildiv((i*nP)+B, f3)
		elif result == 2:
			mMax = ((i*nP)+B)//f3
		print(mMax-mMin)
		if(mMin-mMax == 0):
			break

	print('%X' %mMax)
	

	

if ( __name__ == "__main__" ) :
  # Produce a sub-process representing the attack target.
  target = subprocess.Popen( args   = sys.argv[ 1 ],
                             stdout = subprocess.PIPE, 
                             stdin  = subprocess.PIPE )

  # Construct handles to attack target standard input and output.
  target_out = target.stdout
  target_in  = target.stdin

  mMax = 347773833112666067882250428860237828536284751851937774998301349400582842266125231652144052973844735641707958243515945426514899866621565894750281126530384065592715203455730702689341777829005478835703191583922036885261978659783344533432274604031718486439445004108324023045369998063524769702384465676869902357
  unpad(mMax, 128)
  #m = I2OSP(mMax, 127)
  # Execute a function representing the attacker.
  #attack(sys.argv[2])