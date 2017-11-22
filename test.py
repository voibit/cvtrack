#!/usr/bin/python

import cv2
import numpy as np
import sys

width=1280.
height=720.
hJust=910

""" global vars """
if len(sys.argv) < 4: 
	print("dir outdir vidnr ")
	exit()

vidnr=sys.argv[3]
videofile=sys.argv[1]+vidnr+".mp4" # =0 if webcam
outfile=sys.argv[2]
imgnr=0

#color limits i bgr
lower=[0,0,0]
upper=[0,0,0]
lowerN=[0,0,0]
upperN=[0,0,0]
save=0
neg=0
filt=0
areaLimit=100000

def nothing(x):
	#print(x)
	pass

def setSave(x):
	global save
	save = x
	pass
def setNeg(x):
	global neg
	neg = x
	pass
def setFilt(x):
	global filt
	filt = x
	pass
def setNeg(x):
	global neg
	neg = x
	pass
def setArea(x):
	global areaLimit
	areaLimit=x
	pass

cap = cv2.VideoCapture(videofile)

while not cap.isOpened():
    cap = cv2.VideoCapture(videofile)
    cv2.waitKey(1000)
    print("awaiting video...")

cv2.namedWindow('frame')
cv2.namedWindow('lower')
cv2.namedWindow('upper')
cv2.namedWindow('lower-')
cv2.namedWindow('upper-')
cv2.namedWindow('mask')
cv2.namedWindow('neg')
cv2.moveWindow('frame', 0,40)
cv2.moveWindow('mask', 1500,50)
cv2.moveWindow('neg', 1500,1050)
cv2.moveWindow('lower', 0,hJust)
cv2.moveWindow('upper', 305,hJust)
cv2.moveWindow('lower-', 610,hJust)
cv2.moveWindow('upper-', 915,hJust)

# Create a black image, a window
img = np.zeros((100,300,3), np.uint8)
img2= img.copy()
img3= img.copy()
img4= img.copy()

def sett(x):
    global lower 
    lower[2] = cv2.getTrackbarPos('R1','lower')
    lower[1] = cv2.getTrackbarPos('G1','lower')
    lower[0] = cv2.getTrackbarPos('B1','lower')
    img[:] = lower
    cv2.imshow('lower', img)
    pass


def sett2(x):
    global upper
    upper[2] = cv2.getTrackbarPos('R2','upper')
    upper[1] = cv2.getTrackbarPos('G2','upper')
    upper[0] = cv2.getTrackbarPos('B2','upper')
    img2[:] = upper
    cv2.imshow('upper',img2)
    pass
def sett3(x):
    global lowerN
    lowerN[2] = cv2.getTrackbarPos('R3','lower-')
    lowerN[1] = cv2.getTrackbarPos('G3','lower-')
    lowerN[0] = cv2.getTrackbarPos('B3','lower-')
    img3[:] = lowerN
    cv2.imshow('lower-',img3)
    pass
def sett4(x):
    global upperN
    upperN[2] = cv2.getTrackbarPos('R4','upper-')
    upperN[1] = cv2.getTrackbarPos('G4','upper-')
    upperN[0] = cv2.getTrackbarPos('B4','upper-')
    img4[:] = upperN
    cv2.imshow('upper-',img4)
    pass

cv2.createTrackbar('save','frame',0,1,setSave)
cv2.createTrackbar('sub','neg',0,1,setNeg)
cv2.createTrackbar('filt','mask',0,1,setFilt)
# create trackbars for color change
cv2.createTrackbar('R1','lower',0,255,sett)
cv2.createTrackbar('G1','lower',0,255,sett)
cv2.createTrackbar('B1','lower',0,255,sett)
cv2.createTrackbar('R2','upper',0,255,sett2)
cv2.createTrackbar('G2','upper',0,255,sett2)
cv2.createTrackbar('B2','upper',0,255,sett2)
cv2.createTrackbar('R3','lower-',0,255,sett3)
cv2.createTrackbar('G3','lower-',0,255,sett3)
cv2.createTrackbar('B3','lower-',0,255,sett3)
cv2.createTrackbar('R4','upper-',0,255,sett4)
cv2.createTrackbar('G4','upper-',0,255,sett4)
cv2.createTrackbar('B4','upper-',0,255,sett4)
cv2.createTrackbar('area', 'mask', 10000, 100000, setArea)

cv2.imshow('lower',img)
cv2.imshow('upper',img2)
cv2.imshow('lower-',img3)
cv2.imshow('upper-',img4)

while(1):
    #slowdown
    k = cv2.waitKey()   
    if k == 27: #esc 
        break
    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    bgrL = np.array(lower,np.uint8)
    bgrU = np.array(upper,np.uint8)
    bgrLN = np.array(lowerN,np.uint8)
    bgrUN = np.array(upperN,np.uint8)
    mask = cv2.inRange(hsv, bgrL, bgrU)
    maskN = cv2.inRange(hsv, bgrLN, bgrUN)

    if neg: 
    	mask = cv2.subtract(mask, maskN)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6,8))
    if filt:
	    eroded = cv2.erode(mask, kernel, iterations = 2)
	    mask = cv2.dilate(eroded, kernel, iterations = 3)

    mask = cv2.dilate(mask, kernel, iterations = 2)

    # show image where white in mask 
    #TODO: use eroded-dilated mask

    res = cv2.bitwise_and(frame,frame, mask=mask)

    box=cv2.boundingRect(cv2.findNonZero(mask))

    boxWidth=box[2]
    boxWidthP=boxWidth/width
    boxHeight=box[3]
    boxHeightP=boxHeight/height
    frame2=frame.copy()
    #print(str(boxWidth)+" "+str(boxHeight))

    # calculate position 
    moment= cv2.moments(mask)

    if (moment['m00'] > areaLimit):
		
        posX = moment['m10']/moment['m00']
        posY = moment['m01']/moment['m00']
        posXp = posX/width
        posYp = posY/height
        posX=int(posX)
        posY=int(posY)

        #print ("areal: "+str(moment['m00'])+" x:"+str(posX)+" y:"+str(posY))
  
       	#draw circle to mark found position
        cv2.circle(frame2,(posX,posY),40,255)
        cv2.circle(frame2,(posX,posY),41,255)

        cv2.rectangle(frame2,(int(posX-boxWidth/2),int(posY-boxHeight/2)),(int(posX+boxWidth/2),int(posY+boxHeight/2)),(0,255,0),3)
        if(save):
        	if boxWidthP > 0.1:
        		print("too wide")
        	elif boxHeightP > 0.6:
        		print("too high")
        	else: 
	        
	        	cv2.imwrite("%s%s_%s.jpg"%(outfile,vidnr,imgnr),frame,[cv2.IMWRITE_JPEG_QUALITY ,95])

	        	with open("%s%s_%s.txt"%(outfile,vidnr,imgnr), "a+") as f:
	        		f.write("0 %s %s %s %s"%(posXp,posYp,boxWidthP,boxHeightP))
	        	print("%s%s_%s.jpg saved"%(outfile,vidnr,imgnr))
	        	imgnr+=1
    #show images
    cv2.imshow('frame',frame2)
    cv2.imshow('neg',maskN)
    #cv2.imshow('mask',dilated)
    cv2.imshow('mask',res)

cv2.destroyAllWindows()
