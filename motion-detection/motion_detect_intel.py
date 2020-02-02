# This code is taken from https://software.intel.com/en-us/node/754940
# a tutorial from intel on motion detection using opencv.
# To be modified.
import numpy as np
import cv2
from send_image_to_s3 import upload_image

sdThresh = 20
font = cv2.FONT_HERSHEY_SIMPLEX

def distMap(frame1, frame2):
    """outputs pythagorean distance between two frames"""
    frame1_32 = np.float32(frame1)
    frame2_32 = np.float32(frame2)
    diff32 = frame1_32 - frame2_32
    norm32 = np.sqrt(diff32[:,:,0]**2 + diff32[:,:,1]**2 + diff32[:,:,2]**2)/np.sqrt(255**2 + 255**2 + 255**2)
    dist = np.uint8(norm32*255)
    return dist

# cv2.namedWindow('frame')
# cv2.namedWindow('dist')

#capture video stream from camera source. 0 refers to first camera, 1 referes to 2nd and so on.
cap = cv2.VideoCapture(0)

_, frame1 = cap.read()
_, frame2 = cap.read()

above_thresh = False
i = 0

n = 0
while(True):
    _, frame3 = cap.read()
    rows, cols, _ = np.shape(frame3)
    cv2.imshow('dist', frame3)
    dist = distMap(frame1, frame3)

    frame1 = frame2
    frame2 = frame3

    # apply Gaussian smoothing
    mod = cv2.GaussianBlur(dist, (9,9), 0)

    # apply thresholding
    _, thresh = cv2.threshold(mod, 100, 255, 0)

    # calculate st dev test
    _, stDev = cv2.meanStdDev(mod)
    

    # cv2.imshow('dist', mod)
    # cv2.putText(frame2, "Standard Deviation - {}".format(round(stDev[0][0],0)), (70, 70), font, 1, (255, 0, 255), 1, cv2.LINE_AA)
    if stDev < sdThresh and above_thresh:
        # we just dropped below the threshold reset and trigger sending the image.
        above_thresh = False
        print("Just crossed below!")
        file_name = 'img{:03d}.png'.format(i)
        cv2.imwrite(file_name, frame3)
        upload_image(file_name)

        i += 1
        # send frame3
    elif stDev > sdThresh and not above_thresh:
        # we just crossed the threshold.
        above_thresh = True


    # cv2.imshow('frame', frame2)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()