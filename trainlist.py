#!/usr/bin/python

import os
import sys
import string

listfile= "../darknet/trainlist.txt"
if len(sys.argv) < 2: 
	print("ingen datamapper gitt ")
	exit()

if len(sys.argv) == 3: 
	listfile=sys.argv[2]


folder=sys.argv[1]

if folder[-1:]!="/":
	folder=folder+"/"


with open(listfile, "a+") as f:	        		
	for filename in os.listdir(folder):
		if filename[-4:]==".jpg": #and os.access(folder+filename[-4:]+".txt", os.R_OK)
			f.write(folder+filename+"\n")
print("wrote data to: "+listfile)

