#Tries to look for three clusters.i.e. ELV,SD and OC. 50% traning set and 50% testing set.
import numpy as np
from sklearn.svm import SVC
import scipy as sp

import matplotlib.pyplot as plt
import random
fin=open("SD_ELV_OC_combinedList","r")
a=fin.readlines()
cplcc=[]

cfn=[]
temp=0.0
ctr=0.
for i in a:
	ctr=ctr+1
	if(i[0]=='#'):
		continue
	else:
		temp=i.split()
		cplcc.append([float(temp[2]),float(temp[3])])
		
	if(ctr>618):
		plt.scatter(float(temp[2]),float(temp[3]), color='g',s=4)
		cfn.append(3)
	elif(ctr>463):
		plt.scatter(float(temp[2]),float(temp[3]), color='b',s=4)
		cfn.append(2)
	else:
		plt.scatter(float(temp[2]),float(temp[3]), color='r',s=4)
		cfn.append(1)
r1=random.sample(range(len(cplcc)), len(cplcc)/2)
plt.xlim(0, 30)
plt.xlabel ("CPL") 
#plt.ylim(0.3, 1)
plt.ylabel ("CC")
plt.show()
print r1[1]
tr_s=[]
ts_s=[]
tr_c=[]
ts_c=[]
for i in range (0,len(cplcc)):
	if(i in r1):
		tr_s.append(cplcc[i])
		tr_c.append(cfn[i])
	else:
		ts_s.append(cplcc[i])
		ts_c.append(cfn[i])

	


clf = SVC(gamma='auto')
clf.fit(tr_s, tr_c)
ts_p=clf.predict(ts_s)
ctr2=0
oc_f=0
elv_f=0
sd_f=0
sd_c=0
elv_c=0
oc_c=0
for i in range(0,len(ts_s)):
	#print ts_s[i],ts_c[i],ts_p[i] 
	if(ts_c[i]==ts_p[i]):
		ctr2=ctr2+1
		flag=1
	else:
		flag=0
	if(ts_p[i]==1):
		plt.scatter(ts_s[i][0],ts_s[i][1], color='r',s=4)
		oc_f=oc_f+1
		if(flag==1):
			oc_c=oc_c+1
	elif(ts_p[i]==2):
		plt.scatter(ts_s[i][0],ts_s[i][1], color='b',s=4)
		sd_f=sd_f+1
		if(flag==1):
			sd_c=sd_c+1
	elif(ts_p[i]==3):
		plt.scatter(ts_s[i][0],ts_s[i][1], color='g',s=4)
		elv_f=elv_f+1
		if(flag==1):
			elv_c=elv_c+1
print float(ctr2)/len(ts_s), "predicted correctly"
print float(oc_c)/oc_f, "ocs predicted correctly"
print float(sd_c)/sd_f, "sds predictred correctly"
print float(elv_c)/elv_f, "elvs predicted correctly"
plt.xlim(0, 30)
plt.xlabel ("CPL") 
plt.ylim(0.3, 1)
plt.ylabel ("CC")

plt.show()
