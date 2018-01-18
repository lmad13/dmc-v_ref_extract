import numpy as np
import matplotlib.pyplot as plt
import glob
import sys

ID=sys.argv[1]

#To Make V_ref:
path='results*'+ID+'*'
fileList=glob.glob(path)
nRep=0
for fileName in fileList:
    resultsFile=open(fileName,'r')
    for line in resultsFiles:
        if 'propagating for time' in line:
            nSteps=int(line.split()[3])
            print 'nSteps=', nSteps
            nWfns=int(line.split()[5])
            print 'nWfns=',nWfns

        if 'Repetition Number is' in line:
            n=int(line.split()[3]) 
            nRep=n if n>nRep else nRep

nRep=nRep+1 #nRep will be 9 if there are 10 reps complete



path='V_ref*'+ID+'*'
fileList=glob.glob(path)

#print fileList

count=len(fileList)

print count
averageV1L=[]
averageV1R=[]
averageV0=[]
eqStep=-5
for fileName in fileList:
    #print 'fileName',fileName
    tempData=np.loadtxt(fileName)
    stepNumber=tempData[:,0]
    V1L=tempData[:,1]
    V1R=tempData[:,2]
    V0=tempData[:,3]
    
    averageV1L.append(np.average(V1L[eqStep:]))
    averageV1R.append(np.average(V1R[eqStep:]))
    averageV0.append(np.average(V0[eqStep:]))


print 'V1L-V0=', (np.average(averageV1L)-np.average(averageV0))*219474.63
print 'V1R-V0=', (np.average(averageV1L)-np.average(averageV0))*219474.63
print 'V0=', (np.average(averageV0))*219474.63

fileout=open('Energies.dat', 'w')
fileout.write('V1L-V0= '+str((np.average(averageV1L)-np.average(averageV0))*219474.63)+'   cm^{-1}\n')
fileout.write('V1R-V0= '+str((np.average(averageV1L)-np.average(averageV0))*219474.63)+'   cm^{-1}\n')
fileout.write('V0=     '+str(np.average(averageV0)*219474.63)+'   cm^{-1}\n')
fileout.close()
