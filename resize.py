#!/usr/bin/python

import os
import sys
import string
import cv2
from shutil import copy2

if len(sys.argv) < 3: 
	print("resize.py dir dest")
	exit()


folder=sys.argv[1]
dest=sys.argv[2]

if folder[-1:]!="/":
	folder=folder+"/"

if dest[-1:]!="/":
	dest=dest+"/"

      		
for filename in os.listdir(folder):
	if filename[-4:]==".jpg":
		cv2.imwrite(dest+filename, cv2.resize(cv2.imread(folder+filename), (0,0), fx=0.5, fy=0.5),[cv2.IMWRITE_JPEG_QUALITY ,90])
		copy2(folder+filename[:-4]+".txt",dest)
		print("endret størrelse på "+filename+"\n")
