import sys, subprocess
import math, hashlib

def interact( G ) :
  # Send      G      to   attack target.
  stringver = "%X" % G
  while (len(stringver)) != 256:
    stringver = '0' + stringver
  
  print "Length = %d" % len(stringver)
  target_in.write( "%s\n" % stringver ) ; target_in.flush()
  #print "string sent %s" % stringver
  if(len(stringver) != 256):
        print "string sent %s" % stringver
  # Receive ( t, r ) from attack target.
  r = int( target_out.readline().strip() )

  return r


def ceildiv(a,b):
    return -(-a//b)
    

def pow_mod(x, y, z):
    number = 1
    while y:
        if y & 1:
            number = number * x % z
        y >>= 1
        x = x * x % z
    return number

def attack(publicfile) :
    # Select a hard-coded guess ...
    fp = open(publicfile,'r')
    N = int(fp.readline(),16)
    e = int(fp.readline(),16)
    c = int(fp.readline(),16)
    k = int(math.log(N,256)) + 1
    print k
    B = int(2**(8*(k-1)))
    print "%X" % B
    f1 = 2
    cP = pow_mod(f1,e,N)
    cP = (cP * c) %N
    print "cP = %X\n" % cP
    print "f1 = %d" % f1
    r = interact(cP)
    while r != 1:
        f1 *= 2
        cP = pow_mod(f1,e,N)
        cP = (cP * c) % N
        print "cP = %X\n" % cP
        print "f1 = %d" % f1
        r = interact(cP)


    print "B = %X\n" %B
    print "f1 = %X\n" %f1 
    print "stage 1 r = %X\n"% r
    
    print "stage 1 N = %X\n"% N
    #step2
    f2 = int(((N+B)//B) *  (f1//2))
    print "f2 = %X" % f2
    
    cP = pow_mod(f2,e,N)
    cP = (cP * c) % N
    print "cP = %X\n" % cP
    print "N/B = %X" % (N/B)
    r = interact(cP)
    count = 1
    while r == 1:
        count = count + 1
        cP = pow_mod(f2,e,N)
        cP = (cP * c) % N
       # print "cP = %X\n" % cP
        r = interact(cP)
        f2 = f2 + (f1/2)
        print "f2 = %d" % f2

    print "count = %d" % count
    print "step 2 r = %d" % r 

    #step3 
    mMin = ceildiv(N,f2)
    mMax = ((N+B)//f2)
    print " max = %X \n" % mMax
    print " min = %X \n" % mMin
    print " delta = %X \n" % (mMax-mMin)

    print "part 3 start = %X \n" % (f2 * (mMax - mMin))
    print " B = %X \n" % (B - (f2 * (mMax - mMin)))
    
    print " c = %X \n" % c

    while mMin < mMax:
        mDelta = mMax - mMin
        #print "DELTA = %X" % mDelta
        fTmp = (2*B)//mDelta
        i = (fTmp*mMin)//N
        IN = i*N
        f3 = ceildiv(IN,mMin)
        cP = pow_mod(f3,e,N)
        cP = (cP * c) % N
        #print "cP = %X\n" % cP
        #print "f3 = %d" % f3
        r = interact(cP)
        if(r == 1):
            mMin = int(ceildiv(((IN)+B),f3))
        else:
            print "r = %d" % r
            mMax = int(((IN+B)//f3))
   
    
            
    mMin = int(ceildiv((IN+B),f3))
    print "f3 = %X\n" % f3 
    print "mMin = %X\n " % mMin
    print "mMax = %X \n" % mMax
    print "f3 - B = %X" % (f3-B)
  # Print all of the inputs and outputs.
    print "cP = %X" % ( cP )
    print "r = %d" % ( r )


def MGF(maskedDB,len):
    print "HIII"
    return 24242

def DecryptOAEP (EM,pk) :
    #r = Y XOR Hash(X)
    #message = X XOR GHash(r)
    L = "" # the empty string
    lHash = hash(L)
    #Y is a single octet
    hlen = len(("%X"%lHash))
    maskedDBLength = len(EM) - 1 - hlen
    maskedSeed = EM[1:hlen+1]
    maskedDB = EM[hlen+1:]
    if maskedDBLength != len(maskedDB):
        print "OH NO!\n"
    seedmask = MGF(maskedDB,hlen)
    seed = bool(maskedSeed) ^ bool(seedMask)
    dbMask = MGF(seed,maskedDBLength)
    DB = bool(maskedDB) ^ bool(dbMask)
    lhashprime = DB[:hlen]
    #PS length = 0
    zeroOne = DB[hlen+1:hlen+3]
    print zeroOne
    message = DB[hlen+4:]

    return message

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
