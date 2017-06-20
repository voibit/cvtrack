#!/usr/bin/python

import cv2
import numpy as np
import sys


width=1280.
height=720.

hJust=910
""" global vars """
if len(sys.argv) < 5: 
	print("dir outdir vidnr hypighet")
	exit()

vidnr=sys.argv[3]
videofile=sys.argv[1]+vidnr+".mp4" # =0 if webcam
outfile=sys.argv[2]
hypighet=int(sys.argv[4])
imgnr=0

save=0

cap = cv2.VideoCapture(videofile)

while not cap.isOpened():
    cap = cv2.VideoCapture(videofile)

    cv2.waitKey(1000)
    print("awaiting video...")




while(1):


    # Take each frame
    ok, frame = cap.read()
    if (not ok):
        print("videofil slutt")
        break
    if(imgnr % hypighet == 0):
	        
        cv2.imwrite("%s%s_%s.jpg"%(outfile,vidnr,imgnr),frame,[cv2.IMWRITE_JPEG_QUALITY ,95])

        print("%s%s_%s.jpg saved"%(outfile,vidnr,imgnr))
    imgnr+=1
    cv2.waitKey(10)
    

