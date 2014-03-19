import sys, subprocess, math



def trunc(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    slen = len('%.*f' % (n, f))
    return str(f)[:slen]

def ceildiv(a, b):
	(c,d) = divmod(a,b)
	if(d != 0):
		return a//b + 1
	else:
		return a//b
	#return -(-a//b)
    #return (long(a + (b-1))//long(b))
    #x = long(-a/b)
	#return -(int(math.floor(long(x)) - 1))


def interact( G ) :
	#print(G)
	# Send      G      to   attack target.
	target_in.write( "%s\n" % ( G ) ) ; target_in.flush()

	# Receive ( t, r ) from attack target.
	t = int( target_out.readline().strip() )



	return ( t )


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
	while(result == 1):
		f2New = (pow(f2, eP, nP)*cP)%nP
		f2Hex = hex(int(f2New)).rstrip("L").lstrip("0x") or "0"
		result = (interact(f2Hex.zfill(256)))
		if result == 1 :
			f2 = f2+(f1/2)



	#stage3
	mMin = ceildiv(nP, f2)
	mMax = (nP + B)//f2
	print"mmin = %d\n" %mMin 
	print"mmax = %d\n" %mMax 
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
		if(mMin-mMax == 0):
			break



	print("m^e mod n ")
	print(pow(mMin,eP,nP))
	print(" c -")
	print(int(c, 16))	

if ( __name__ == "__main__" ) :
  # Produce a sub-process representing the attack target.
  target = subprocess.Popen( args   = sys.argv[ 1 ],
                             stdout = subprocess.PIPE, 
                             stdin  = subprocess.PIPE )

  # Construct handles to attack target standard input and output.
  target_out = target.stdout
  target_in  = target.stdin

  # Execute a function representing the attacker.
  attack(sys.argv[2])