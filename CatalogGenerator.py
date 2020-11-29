fin=open("AlphasGammas_OCBinaries.dat","r")
ocb=fin.readlines()
ocborder=[]
for i in range (0,len(ocb)):
	temp=ocb[i].split()
	temp2=temp[0].split("_")
	temp3=temp2[1][4:13]
	ocborder.append(temp3)
fin2=open("KeplerCatalogV3.csv","r")
fin3=open("OC_CB","r")
fouterr3=open("Catalog3Err.dat","w")
fouterr2=open("Catalog2Err.dat","w")
kv3=fin2.readlines()
kv2=fin3.readlines()
v2_l=[]
v3_l=[]
nmf=1.
v2f=1.
v3f=1.
flag2=1
flag3=1
for nm in ocborder:
	nmf=float(nm)
	for nm1 in kv3:
		temp=nm1.split()
		v3f=float(temp[0])
		if(v3f==nmf):
			v3_l.append(nm1)
			flag3=0
	for nm2 in kv2:
		temp=nm2.split()
		v2f=float(temp[0])
		if(v2f==nmf):
			v2_l.append(nm2)
			flag2=0
	if(flag3==1):
		v3_l.append("0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t\n")
		fouterr3.write(nm+" not found in Catalog 3\n")
	if(flag2==1):
		fouterr2.write(nm+" not found in Catalog 2\n")
	flag2=1
	flag3=1
		
len(v2_l)==len(v3_l)
for i in range (0,len(v3_l)):
	v3_l[i]=v3_l[i].strip('\n')
	v2_l[i]=v2_l[i].strip('\n')
	ocb[i]=ocb[i].strip('\n')
foutcat=open("ComplexityCatalog_v1.dat","w")
for i in range (0,len(ocborder)):
	foutcat.write(ocb[i]+'\t'+v2_l[i]+'\t'+v3_l[i]+'\n')

