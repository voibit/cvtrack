#!/usr/bin/python

import os
import sys
import string
import random
picnr=0

if len(sys.argv) < 2: 
	print("ingen mappe gitt ")
	exit()


def randid(N=3, s=string.ascii_uppercase + string.digits):
	return ''.join(random.SystemRandom().choice(s) for _ in range(N))

for filename in os.listdir(sys.argv[1]):
	if filename[-4:]==".jpg":

		if (picnr%2):
			#os.rename(filename, str(start)+filename[-4:])
			rand=randid()
			os.rename(filename,rand+"_"+filename)
			os.rename(filename[:-4]+".txt",rand+"_"+filename[:-4]+".txt")
			start +=1
		else:
			os.remove(filename)
			os.remove(filename[:-4]+".txt")
		picnr+=1
