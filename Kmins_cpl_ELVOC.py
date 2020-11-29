import scipy as sp
import scipy.cluster.vq as spv
import matplotlib.pyplot as plt
import numpy as np
#%matplotlib inline
#import pandas as pd
fin=open("SD_OC_combinedList","r")
a=fin.readlines()
cpl=[]
cc=[]
adeg=[]
cfn=[]
temp=0.0
ctr=0.
colmap = {1: 'r', 2: 'g'}
for i in a:
	ctr=ctr+1
	if(i[0]=='#'):
		continue
	else:
		temp=i.split()
		adeg.append(float(temp[1]))
		cpl.append(float(temp[2]))
		cc.append(float(temp[3]))
	if(ctr>464):
		cfn.append("SD")
	else:
		cfn.append("OC")
df=np.zeros((len(cc),2))
df2=np.zeros((len(cc)))
for j in range (0,len(cc)):
	df[j][0] = cpl[j]
	df[j][1] = cc[j]
	df2[j] = cpl[j]	
ctrpo=0
ctrps=0

for j in range(0,len(df)):
	#print len(df), j, df[j]
	if(df[j][0]>9.8):
	
		if(cfn[j]=="OC"):
			ctrpo=ctrpo+1
	else:
		if(cfn[j]=="SD"):
			ctrps=ctrps+1
print "CPL alone OC false positives", ctrpo," ELV ",ctrps 

#print codebook
#plt.scatter(whitened[:, 0], whitened[:, 1], c='g')
#plt.scatter(codebook[:, 0], codebook[:, 1], c='r')
#plt.show()
#print centroids

whitened2 = spv.whiten(df2)
centroids2,labels2 = spv.kmeans2(whitened2, 2,iter=100)
ctrs=0
ctro=0
for j in range (0,len(df2)):
	if(labels2[j]==0):
		
		if(cfn[j]=="OC"):
			ctro=ctro+1
	else:
		
		if(cfn[j]=="SD"):
			ctrs=ctrs+1
print ctrs, "is true positives for ELV and",ctro,"is true positive for OC"
