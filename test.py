import cv2
import numpy as np

#color limits in hsv 
lower=[0,0,0]
upper=[0,0,0]

def nothing(x):
    #print(x)
    pass

cap = cv2.VideoCapture("./tst.mp4")


while not cap.isOpened():
    cap = cv2.VideoCapture("./tst.mp4")
    cv2.waitKey(1000)
    print("Venter på video..")


cap.set(3,320) 
cap.set(4,240)

cv2.namedWindow('frame')
cv2.namedWindow('lower')
cv2.namedWindow('upper')
cv2.namedWindow('mask')
cv2.namedWindow('filtered')
cv2.namedWindow('res')

cv2.moveWindow('frame', 0,0)
cv2.moveWindow('mask', 0,400)
cv2.moveWindow('filtered', 400,400)
cv2.moveWindow('res', 0,800)
cv2.moveWindow('lower', 450,0)
cv2.moveWindow('upper', 755,0)

# Create a black image, a window
img = np.zeros((100,300,3), np.uint8)
img2 = np.zeros((100,300,3), np.uint8)



def sett(x):
    global r1, g1, g2
    lower[0] = cv2.getTrackbarPos('R1','lower')
    lower[1] = cv2.getTrackbarPos('G1','lower')
    lower[2] = cv2.getTrackbarPos('B1','lower')


    img[:] = [b1,g1,r1]
    cv2.imshow('lower',img)
    pass

def sett2(x):
    global r2, g2, b2
    upper[0] = cv2.getTrackbarPos('R2','upper')
    upper[1] = cv2.getTrackbarPos('G2','upper')
    upper[2] = cv2.getTrackbarPos('B2','upper')

    img2[:] = [b2,g2,r2]
    cv2.imshow('upper',img2)
    pass




cv2.createTrackbar('save','frame',0,1,nothing)
# create trackbars for color change
cv2.createTrackbar('R1','lower',0,255,sett)
cv2.createTrackbar('G1','lower',0,255,sett)
cv2.createTrackbar('B1','lower',0,255,sett)

cv2.createTrackbar('R2','upper',0,255,sett2)
cv2.createTrackbar('G2','upper',0,255,sett2)
cv2.createTrackbar('B2','upper',0,255,sett2)

cv2.imshow('lower',img)
cv2.imshow('upper',img2)

while(1):



    #slowdown
    k = cv2.waitKey()   
    if k == 27: #esc 
        break


    # Take each frame
    _, frame = cap.read()

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, np.array(lower), np.array(upper))

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6,6))

    eroded = cv2.erode(mask, kernel, iterations = 2)
    dilated = cv2.dilate(eroded, kernel, iterations = 1)
    

    # show image where white in mask 
    res = cv2.bitwise_and(frame,frame, mask=mask)
 
    # calculate position 
    moment= cv2.moments(dilated)

    if (moment['m00'] > 100000):
        posX = moment['m10']/moment['m00']
        posY = moment['m01']/moment['m00']

        print ("areal: "+str(moment['m00'])+" x:"+str(posX)+" y:"+str(posY))
       	#draw circle to mark found position
        cv2.circle(frame,(int(posX),int(posY)),40,255)
        cv2.circle(frame,(int(posX),int(posY)),41,255)


    #show images
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('filtered',dilated)
    cv2.imshow('res',res)


cv2.destroyAllWindows()