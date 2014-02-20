import sys,commands

class StageError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def checkStage(stage):
    flag = True
    cmd = commands.getoutput('./modmul stage'+str(stage)+' < stage'+str(stage)+'.input')
    cmd = cmd.split()

    if (len(cmd)==0):
        raise StageError('This stage did not return any output')

    for idx, item in enumerate(cmd):
        cmd[idx] = cmd[idx]
        cmd[idx] = cmd[idx].upper()

    stagename = 'stage'+str(stage)+'.output'
    correct = open(stagename, 'r')
    correct = correct.read()
    correct = correct.split()

    for idx, item in enumerate(correct):
        try:
            whatC = 'c'+str((idx%2)+1)
            if (correct[idx] != cmd[idx]):
                if(stage==3):
                    print('Error in stage %d, case %d: %s is Wrong' % (stage,(idx+2)/2,whatC))
                else:
                    print('Error in stage %d, case %d'%(stage,(idx+1)))
                print('Test:\t '+cmd[idx])
                print('Correct: '+correct[idx])
                flag = False
        except IndexError:
            raise StageError('You do not have enough output. Do more.')
    return flag

passed = True

for i in range(1,5):
    try:
        if checkStage(i):
            print('Stage '+str(i)+': PASS')
        else:
            passed = False
            print('Stage '+str(i)+': FAIL')
    except StageError as e:
        print('Stage '+str(i)+': '+e.value)
