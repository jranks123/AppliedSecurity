import sys, subprocess, math
from decimal import *

def iround(x):
    """iround(number) -> integer
    Round a number to the nearest integer."""
    return int(round(x) - .5) + (x > 0)


def trunc(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    slen = len('%.*f' % (n, f))
    return str(f)[:slen]


def interact( G ) :
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
	B = pow(2, 8*(k-1))


	f1 = 1
	result = 0
	while result != 1:
		f1 = f1*2
		result = pow(f1, eP, nP)
		result = (result*cP)%nP
		result = hex(result).rstrip("L").lstrip("0x") or "0"
		result = (interact(result.zfill(256)))

	f2 = int(math.floor(((nP+B)/B))*(f1/2))
	while(result == 1):
		f2Hex = hex(f2).rstrip("L").lstrip("0x") or "0"
		result = (interact(f2Hex.zfill(256)))
		if result == 1 :
			f2 = f2+(f1/2)


	f2 = Decimal('%.2f' % f2)
	B = Decimal('%.2f' % B)
	mMin = nP/f2
	mMax = Decimal((nP + B)/f2)
	result = 1
	while(math.fabs(mMax-mMin)>0):
		fTmp = (2*B)//(mMax-mMin)
		i = (fTmp*mMin)
		i = (Decimal(i)//Decimal(nP))
		f3 = int(math.ceil((i*nP)/mMin))
		f3Hex = hex(f3).rstrip("L").lstrip("0x") or "0"
		result = (interact(f3Hex.zfill(256)))
		if result == 1:
			mMin = (Decimal((i*Decimal(nP))+B)/f3)
			mMin.to_integral_exact(rounding=ROUND_CEILING)	
		else:
			mMax = (((i*Decimal(nP))+B)/f3)
			mMin.to_integral_exact(rounding=ROUND_FLOOR)	

		print(mMax-mMin)
		#print(mMin)
		#print(mMax)
		#print(" ")

		if(mMin==mMax):
			print("OMG")
			break

			





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