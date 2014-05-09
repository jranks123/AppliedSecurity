import sys, subprocess, math, os, random, platform, numpy, string
def generateHex() :
	lst = [random.choice(string.hexdigits) for n in xrange(32)]
	cHex = "".join(lst)
	return cHex


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


def interact(m) :

	# Send      G      to   attack target.
	target_in.write( "%s\n" % ( m )) ; target_in.flush()
	# Receive ( t) from attack target.
	traces = ( target_out.readline().strip() )
	c = ( target_out.readline().strip() )
	
	return traces, c

def getHammingWeight(b):
	return bin(b).count('1')


def getArray(t):
	tArray = t.split( "," )
	return tArray


def tuple_without(original_tuple, element_to_remove):
    new_tuple = []
    for s in list(original_tuple):
        if not s == element_to_remove:
            new_tuple.append(s)
    return tuple(new_tuple)

def limitArray(t, lowBound, upperBound):
	print "Original T Length= " + str(len(t[0]))
	print("range = " + str(upperBound - lowBound))
	print("lowBound = " + str(lowBound))
	print("upperBound = " + str(upperBound))
	newArray = []
	for j in range(0,10):
		newT = []
		for i in range (lowBound, upperBound):
		#	print t
		#	print ("i = " + str(i))
		#	print ("j = " + str(j))
			newT.append(t[j][i])
		newArray.append(newT)
	print("length of new T = " + str(len(newT)))
	print
	return newArray

def limitT(t, lowBound, highBound):
	newT = []
	for i in range (lowBound, highBound):
		newT.append(t[i])
	return newT


def getPeak(cRow):
	currentHigh = 0
	currentPosition = 0
	for i in range (0, 50):
		if cRow[i] > currentHigh:
			currentHigh = cRow[i]
			currentPosition = i
	return (currentHigh, currentPosition) 



def  dfa(mLow, mHigh, traces, messages):

	b = 1
	tracesLen = len(traces)
	n = len(traces[0])
	after_sbox = numpy.zeros((tracesLen, 256))
	for i in range (0, tracesLen):
		for j in range(0, 256):
			after_sbox[i][j] = sbox[int(messages[i][mLow:mHigh], 16) ^ j]

	key_trace = numpy.zeros((256, n))


	power_consumption = numpy.zeros((tracesLen, 256))
	for i in range (0, len(after_sbox)):
		for j in range(0, len(after_sbox[i])):
			power_consumption[i][j] = getHammingWeight(int(after_sbox[i][j]))

	peakPosition = 0
	highestNum = 0
	potentialByte = 0
	highestNum = 0
	chunksize = 50
	chunks = n/50
	highestRow = 0

	#python pool


	for i in range(0, 256):
		for j in range(0, chunks):
			traceArray = []
			for t in traces:
				traceArray.append(t[j*chunksize:(j+1)*chunksize])
			powArray = []
			for p in power_consumption:
				powArray.append(p[i:i+1])
			traceArray = numpy.reshape(traceArray, (tracesLen, chunksize))
			powArray = numpy.reshape(powArray, (tracesLen, 1))
			cmatrix = numpy.corrcoef(traceArray, powArray, 0)
			cmatrix = zip(*cmatrix)
			(currentHigh, potentialPeakPosition) = getPeak(cmatrix[50:][0][:50])
			if currentHigh > highestNum:
				peakPosition = (j*chunks)+ potentialPeakPosition
				highestNum = currentHigh
				highestRow = i

	print "KEY = " + str(highestRow)
	return peakPosition
			
def dfaQuad(k1, k2, k3, k4, lowBound, upperBound, traces, messages):
	lowTemp = lowBound
	lowBound = dfa(k1,k2, traces, messages)
	print "LOWER BOUND DISCOVERED = " + str(lowBound)
	upperBound = upperBound - lowTemp 
	traces = limitArray(traces, lowBound, upperBound)
	upperBound = dfa(k3,k4,traces, messages)
	print
	print "Upper BOUND DISCOVERED = " + str(upperBound)
	traces = limitArray(traces, 0, upperBound)
	return (lowBound, upperBound, traces, messages)


def attack():
	lowBound = 900
	upperBound = 1500
	traces = []
	messages = []
	for i in range(0, 10):
		m = generateHex()
		t, c = interact(m)
		t = getArray(t)
		t = limitT(t, lowBound, upperBound)
		traces.append(t)
		messages.append(m)

	(lowBound, upperBound, traces, messages) = dfaQuad(0,2,30,32,lowBound, upperBound, traces, messages)
	(lowBound, upperBound, traces, messages) = dfaQuad(2,4,28,30,lowBound, upperBound, traces, messages)
	(lowBound, upperBound, traces, messages) = dfaQuad(4,6,26,28,lowBound, upperBound, traces, messages)
	(lowBound, upperBound, traces, messages) = dfaQuad(6,8,24,26,lowBound, upperBound, traces, messages)
	(lowBound, upperBound, traces, messages) = dfaQuad(8,10,22,24,lowBound, upperBound, traces, messages)
	(lowBound, upperBound, traces, messages) = dfaQuad(10,12,20,22,lowBound, upperBound, traces, messages)
	(lowBound, upperBound, traces, messages) = dfaQuad(12,14,18,20,lowBound, upperBound, traces, messages)
	(lowBound, upperBound, traces, messages) = dfaQuad(14,16,16,18,lowBound, upperBound, traces, messages)
	

	#lowTemp = lowBound
	#lowBound = dfa(2,4,traces, messages)
#	upperBound = upperBound - lowTemp
#	traces = limitArray(traces, lowBound, upperBound)
#	upperTemp = dfa(12,14,traces, messages)



if ( __name__ == "__main__" ) :
  # Produce a sub-process representing the attack target.
	target = subprocess.Popen( args   = sys.argv[ 1 ],
                             stdout = subprocess.PIPE, 
                             stdin  = subprocess.PIPE )
	target_out = target.stdout
	target_in  = target.stdin

  # Construct handles to attack target standard input and output.
	attack()
