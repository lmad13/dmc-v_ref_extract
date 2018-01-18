import numpy as np
import matplotlib.pyplot as plt
import glob
import sys

ID=sys.argv[1]
au2wn=219474.63 #cm-1*/(a.u.)
#To Make V_ref:
path='results*'+ID+'*'
fileList=glob.glob(path)
nRep=0

resultsFile=open(fileList[0],'r')
for line in resultsFile:
    if 'propagating for time' in line:
        nSteps=int(line.split()[3])
        print 'nSteps=', nSteps
        nWfns=int(line.split()[5])
        print 'nWfns=',nWfns
        
    if 'Repetition Number is' in line:
        n=int(line.split()[3]) 
        nRep=n if n>nRep else nRep

resultsFile.close()
nRep=nRep+1 #nRep will be 9 if there are 10 reps complete
nSteps=nSteps+1 #because n+1 are printed (25 prop steps=>26 numbers)

print 'there are ', nRep,'repetitions'
V_ref=np.zeros((nWfns, 3, nRep*len(fileList),nSteps)) 
#Structure: number of wavefunctions, number of repetitions, number of propagation steps, number of states (ground,V1left, v1right)
stateDict={}
stateDict['0ground']=0
stateDict['1left']=1
stateDict['1right']=2
for n,fileIn in enumerate(fileList):
    resultsFile=open(fileIn,'r')
    frep=int(fileIn.split('-')[3].split('.')[0])-1  #split by - then by .
    print fileIn
    for line in resultsFile:
        if "state:" in line:
            state=line.split()[1]+line.split()[3]
        if "for wavefunction number" in line:
            iwfn=int(line.split()[7])
            rep=int(line.split()[3])
            irep=nRep*frep+rep
        if "DISCRETE:" in line:
            istep=int(line.split()[4])
            #print iwfn,stateDict[state],istep,';',nRep,'x',frep,'+',rep,'=',irep
            V_ref[iwfn,stateDict[state],irep,istep]=float(line.split()[6])

    resultsFile.close()
V_ref=V_ref*au2wn
averageV=np.zeros((nWfns,3))
averageV_w_s=np.average(V_ref,axis=(2,3))
print averageV.shape
print 'MIN: ',np.min(averageV_w_s[:,0]),np.min(averageV_w_s[:,1]),np.min(averageV_w_s[:,2])
print 'MAX: ',np.max(averageV_w_s[:,0]),np.max(averageV_w_s[:,1]),np.max(averageV_w_s[:,2])
print 'UNC: ',uncertainityV_s

uncertainityV_s=[(np.max(averageV_w_s[:,0])-np.min(averageV_w_s[:,0]))/(2*np.sqrt(nWfns)),(np.max(averageV_w_s[:,1])-np.min(averageV_w_s[:,1]))/(2*np.sqrt(nWfns)),(np.max(averageV_w_s[:,2])-np.min(averageV_w_s[:,2]))/(2*np.sqrt(nWfns))]
averageV_s=np.average(V_ref,axis=(0,2,3))
print 'AVE: ', averageV_s

deltaE=[averageV_s[1]-averageV_s[0],averageV_s[2]-averageV_s[0]]
unc_delta_E=[np.sqrt(),np.sqrt()]
