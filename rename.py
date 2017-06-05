#!/usr/bin/python

import os
import sys
import string
import random
picnr=0

if len(sys.argv) < 2: 
	print("ingen mappe gitt ")
	exit()

folder=sys.argv[1]

def randid(N=3, s=string.ascii_uppercase + string.digits):
	return ''.join(random.SystemRandom().choice(s) for _ in range(N))

for filename in os.listdir(folder):
	if filename[-4:]==".jpg":

		if (picnr%2):
			#os.rename(filename, str(start)+filename[-4:])
			rand=randid()
			os.rename(folder+filename,folder+rand+"_"+filename)
			os.rename(folder+filename[:-4]+".txt",folder+rand+"_"+filename[:-4]+".txt")
		else:
			os.remove(folder+filename)
			os.remove(folder+filename[:-4]+".txt")
		picnr+=1
