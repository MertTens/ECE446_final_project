#!/Library/Frameworks/Python.framework/Versions/3.6/bin/python3
import numpy.core.multiarray
import time
import math
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Represents image

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray2 = numpy.flip(gray,1)

    print(gray2.shape)
    print(gray2[0][0])
    print(gray2[360][0])
    # Display the resulting frame
    cv2.imshow('frame',gray2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

