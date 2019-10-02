#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
import numpy.core.multiarray
import time
import math
import cv2


scale_percent = 1

cap = cv2.VideoCapture(0)


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Represents image

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray2 = numpy.flip(gray,1)
    
    width = int(gray2.shape[1] * scale_percent / 100)    
    height = int(gray2.shape[0] * scale_percent / 100)    
    dim = (width, height)

    resized = cv2.resize(gray2, dim, interpolation = cv2.INTER_AREA)

    print()
    print()
    print(resized)

    # Display the resulting frame
    cv2.imshow('frame',resized)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

