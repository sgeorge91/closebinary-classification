//Edgelist
#include<iostream>
#include <fstream>
#include <math.h>
#include<stdlib.h>
#include<string>

#include <sstream>
/*This program reads a four column file name from the command line, reads the embedded vectors and generates the edge list*/
using namespace std;
int el[10000][10000];
int main(int argc, char* argv[])
{
ifstream fin;
ofstream fout,fout2;
int N;
int T;
static int ds[20000];
static float dd[20000];

static float x1[20000],x2[20000],x3[20000],x4[20000];
float eps,d;
string fn,fnp,fnpp;

if (argc<4)
{
cout<<"Usage ./el.out  <Fname> <#points> <epsilon>"<<endl;
return(0);
}
else
{
fn=argv[1];
N=stof(argv[2]);
eps=stof(argv[3]);
cout<<"N is"<<N;
}

fin.open(fn);
//reading from file
for(int i=0;i<N;i++)
{

fin>>x1[i]>>x2[i]>>x3[i]>>x4[i]; //stof?
}
//reduces 1 from degree sequence
for (int i=0;i<N;i++)
{
ds[i]=-1;
}
cout<<"Epsilon is"<<eps;
fnpp="el_";
fnp=fnpp+=fn;
cout<<"\n Output file is"<<fnp<<endl;
//fout2.open(fnp);
for (int i=0;i<N;i++)
{
	for (int j=i;j<N;j++)
	{
	d=pow(pow(x1[j]-x1[i],2)+pow(x2[j]-x2[i],2)+pow(x3[j]-x3[i],2)+pow(x4[j]-x4[i],2),.5);
		if(d<eps)
		{
		//cout<<i<<'\t'<<j<<endl;
		if(i!=j)
			{
			el[i][j]=1;
			//fout2<<i<<'\t'<<j<<'\n';
			ds[i]=ds[i]+1;
			}
		}
		else
		{
		//cout<<i<<"\t\t"<<j<<endl;
		el[i][j]=0;
		}
	}
}
fout2.close();
//writes edgelist to file
/*for(int i=0;i<N;i++) COmmented out on 10 Aug 2018 SVG
for(int j=i;j<N;j++)
{
if(el[i][j]==1)
fout2<<i<<'\t'<<j<<'\n';
}
fout2.close();
fout.close();*/

//Makes degree distribution from sequence
for(int i=1;i<N;i++)
	for(int j=i;j<N;j++)	
	{
	if(ds[j]==i)
		{
		T++;		
		dd[i]++;
		}
	}
cout<<"T is"<<T<<"N is"<<N;
//Divides by total degree
for (int i=1;i<N;i++)
{
dd[i]=dd[i]/T;
}
fnpp="dd_";
fnp=fnpp+=fn;
fout.open(fnp);
//writes degree distribution to file
for(int i=0;i<N;i++)
{
fout<<i<<'\t'<<dd[i]<<'\n';
}
fin.close();
return(0);
}
