#This version takes a time series, trunctates it to a lenth, leng and segments it into ns segments. Fourier transforms are taken for each such segment. The powerspectrum is calculated and stored in a file, ps_filename.dat.The Bispectrum is calculated and Normalized till the frequency where the f*P(f) falls to 1/100th of its maximum value. The normalised Bispectrum in units of primary frequency and regular frequency units are written to file.
import numpy as np
import math
import time as tm
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

if(len(b)<3000):
	leng=len(b)-1
	NN=len(b)-1
else:
	leng=3000
	NN=3000

fout_sig=open("RN_ELV_CleanedStars.dat","w")
file_list=glob.glob("ud_*.dat")
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
	os.system ("./EL.out em_"+fn+" "+str(NN)+" "+str(epsilon))
	print "./EL.out em_"+fn+" "+str(NN)+" "+str(epsilon)
	g1p=gt.Graph(directed=False)
	print "Creating graph"
	n_ver=len(em_at1)
	print "Total verices is",n_ver
	for i in range(0,int(n_ver)):
		g1p.add_vertex()
	fil="el_em_"+fn			#raw_input("Enter edgelist")
	fin=open(fil,"r")
	el=fin.readlines()
	temp=0
	print "Total edges are",len(el)
	for i in range(0,len(el)):
		temp=el[i].split()
		g1p.add_edge(int(temp[0]),int(temp[1]))
	l1=gtop.label_largest_component(g1p)
	g1=gtop.GraphView(g1p,vfilt=l1)
	print "Calculating clustering for largest component"
	cl=gcl.local_clustering(g1)	
	clf=gcl.local_clustering(g1p)
	clfa=clf.get_array()
	cla=cl.get_array()
	avg_clus=np.mean(cla)
	avg_clusf=np.mean(clfa)
	print "Average Clustering for largest component is", avg_clus, "and for full graph is", avg_clusf


	dist=gtop.shortest_distance(g1)
	tot_pl=0.0
	print "Calculating average path length"
	
	large_comp=g1.num_vertices()
	print large_comp
	avg_pl = float(sum([sum(i) for i in dist]))/(g1.num_vertices()**2-g1.num_vertices())
	
	fout_measures=open("GraMes_"+fn,"w")
	n_edges=len(el)
	density=(2*n_edges)/(float(n_ver)*(n_ver-1))
	avg_deg=(2*n_edges)/float(n_ver)
	print "CPL is", avg_pl
	gc=gcl.global_clustering(g1)
	gclf=gcl.global_clustering(g1p)
	print "Global clustering for largest component is", gc[0], "and for full graph is", gclf[0]
	fout_measures.write("Vertices:\t"+str(n_ver)+"\nEdges:\t"+str(n_edges)+"\n")
	fout_measures.write("Density:\t"+str(density)+"\nAverage Degree:\t"+str(avg_deg)+"\n")
	fout_measures.write("CPL:\t"+str(avg_pl)+"\n Avg Clustering Largest Comp: \t"+str(avg_clus)+"\n Global Clustering Largest Comp: \t"+str(gc[0])+" Stdev:"+str(gc[1])+"\nAvg Clustering Full Graph:\t"+str(avg_clusf)+"\nGlobal CLustering Full graph:\t"+str(gclf[0])+'\n')


	fout_sig.write(str(temp_fil[1][4:len(temp_fil[1])])+'\t'+str(n_ver)+'\t'+str(n_edges)+'\t'+str(density)+'\t'+str(avg_deg)+'\t'+str(avg_pl)+'\t'+str(avg_clus)+'\t'+str(gc[0])+'\t'+'+-'+'\t'+str(gc[1])+'\t'+str(avg_clusf)+'\t'+str(gclf[0])+'\n')
	
	os.rename("el_em_"+fn,"./ReccNetwork/el_em_"+fn)
	os.rename("GraMes_"+fn,"./ReccNetwork/GraMes_"+fn)
	os.rename("em_"+fn,"./ReccNetwork/em_"+fn)
	
