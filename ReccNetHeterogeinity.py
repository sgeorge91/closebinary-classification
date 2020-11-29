#This version finds the degree distribution and heretogeinity of time series
import numpy as np
import math
import sys
import time as tm
import subprocess as sbp
import graph_tool as gt
import graph_tool.clustering as gcl
import graph_tool.topology as gtop
from numpy import conjugate,absolute
import matplotlib.pyplot as plt
import readline, glob
import os
def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]

readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(complete)


def embedder(fn,ch):
	#function to embed an attractor using mutual information or autocorrelation
	
	
	opt='a'
	t1=[]
	tau=1
	temp1=0
	temp2=0
	temp3=0
	if(ch=='c'):
		fn="Com_"+fn
	else:
		fn=fn
	fin=open(fn,"r")
	
	if (opt=='a'):
		os.system ("./corr "+fn+" -o temper -D 200")
		fin1=open("temper","r")	
		t1=fin1.readlines()
	
		for i in range (2,len(t1)-2):
			temp1=t1[i].split()
			
			if(float(temp1[1])<0.36787944117):
				tau=temp1[0]
				break
		fin1.close()
	print tau

	fin=open(fn,"r")
	a=fin.readlines()
	a=a[0:NN]
	for i in range (0,len(a)):
		a[i]=a[i].strip()
	fout=open("em_"+fn,"w")
	tau=int(tau)
	dim=4
	em_at=np.zeros((len(a)-((dim-1)*tau),dim))
	for i in range(0,len(a)-((dim-1)*tau)):
		for j in range (0,dim):
			em_at[i][j]=a[i+(j*tau)]
	np.savetxt("em_"+fn,em_at, delimiter='\t')
	#Move it into a new folder
	return em_at
#Done till this point



fout_sig=open("Het_SD_CleanedStars.dat","w")
file_list=glob.glob("ud_*.dat")
print "Number of files:",len(file_list)
for fn in file_list:
	b=np.loadtxt(fn)
	l1=len(b)
	print fn
	print "Length of file is",len(b)
	temp_fil=fn.split("_")
	if(len(b)<3000):
		leng=len(b)-1
		NN=len(b)-1
	else:
		leng=3000
		NN=3000
	#leng=int(float(temp_fil[2][2:6])*float(temp_fil[3][2:4]))
	#leng=input(". Enter length to truncate to. ")
	a=b[0:leng]
	ts=.0204#input("Sampling period")
	print "Length of dataset is", len(a), ". Please ensure this  is a power of 2."

	loc_time=tm.strftime("%Y-%m-%d")
	fa=[]
	fs=1.0/ts
	print "Maximum frequency is", fs

	#ns=int(temp_fil[3][2:4])#input("Number of segments")

	#Reduces the average from the whole time series
	file_mean=np.mean(a)
	print file_mean
	for i in range (0,leng):
		a[i]=a[i]-file_mean
	
	epsilon=.14
	
	#fn1="ud_"+fn
	udc="u" #This option is brought forward from a previous version that had an option to not have uniform deviates
	#if(udc=="u")or(udc=="U"):
	#	os.system ("./UD.out "+fn+" "+str(NN))
	#	fn1="ud_"+fn
	em_at1=embedder(fn,udc)
	#if(udc=="u")or(udc=="U"):
	os.system ("./ELDD.out em_"+fn+" "+str(NN)+" "+str(epsilon))
	print "./ELDD.out em_"+fn+" "+str(NN)+" "+str(epsilon)
	p1=sbp.Popen('./Het.out',stdin=sbp.PIPE,shell=True)
	p1.communicate("dd_em_"+fn)
	sys.stdout.flush()
	sys.stdin.flush()
	finhet=open("Het_Measuredd_em_"+fn)
	a1=finhet.readlines()
	temphet=a1[2].split()
	het=temphet[2]
	fout_sig.write(str(temp_fil[1][4:len(temp_fil[1])])+'\t'+str(het)+'\n')
	print str(temp_fil[1][4:len(temp_fil[1])])+'\t'+str(het)+'\n'
	
	os.rename("dd_em_"+fn,"./Het/dd_em_"+fn)
	os.rename("Het_Measuredd_em_"+fn,"./Het/Het_Measuredd_em_"+fn)
	
	
