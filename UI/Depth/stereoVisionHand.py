import sys
import cv2
import numpy as np
import time
import imutils
from matplotlib import pyplot as plt
from cvzone.HandTrackingModule import HandDetector


# Function for stereo vision and depth estimation
import HSV_filter as hsv
import triangulation as tri
import calibration

# Mediapipe for face detection
import mediapipe as mp
import time


hand_detection_right = HandDetector(detectionCon=0.8, maxHands=2)
hand_detection_left = HandDetector(detectionCon=0.8, maxHands=2)
#Problematica que mano elige
mp_draw = mp.solutions.drawing_utils

# Open both cameras
cap_right = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap_left =  cv2.VideoCapture(2, cv2.CAP_DSHOW)


# Stereo vision setup parameters
frame_rate = 120    #Camera frame rate (maximum at 120 fps)
B = 9               #Distance between the cameras [cm]
f = 8              #Camera lense's focal length [mm]
alpha = 56.6        #Camera field of view in the horisontal plane [degrees]




while(True):
    i = 0

    ret_right, frame_right = cap_right.read()
    ret_left, frame_left = cap_left.read()

################## CALIBRATION #########################################################

    #frame_right, frame_left = calib.undistorted(frame_right, frame_left)

########################################################################################

    # If cannot catch any frame, break
    if ret_right == False or ret_left == False:
        break

    else:


        # Result-frames after applying HSV-filter mask
        res_right = cv2.bitwise_and(frame_right, frame_right, mask=mask_right)
        res_left = cv2.bitwise_and(frame_left, frame_left, mask=mask_left)

        # APPLYING SHAPE RECOGNITION:
        hand_right, frame_right = hand_detection_right.findHands(frame_right)
        hand_left, frame_left  = hand_detection_left.findHands(frame_left)

        # Hough Transforms can be used aswell or some neural network to do object detection


        ################## CALCULATING BALL DEPTH #########################################################
        if hand_right[0]["type"] != hand_left[0]["type"] and len(hand_left) > 1:
            i = 1

        # If no ball can be caught in one camera show text "TRACKING LOST"
        if hand_right and hand_left:
            #Nos quedamos con la misma mano

            if hand_right[0]["type"] == hand_left[i]["type"]:

                # Function to calculate depth of object. Outputs vector of all depths in case of several balls.
                # All formulas used to find depth is in video presentaion
                depth = tri.find_depth(hand_right[0]["center"], hand_left[i]["center"], frame_right, frame_left, B, f, alpha)

                cv2.putText(frame_right, "TRACKING", (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124, 252, 0), 2)
                cv2.putText(frame_left, "TRACKING", (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (124, 252, 0), 2)
                cv2.putText(frame_right, "Distance: " + str(round(depth, 3)), (200, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (124, 252, 0), 2)
                cv2.putText(frame_left, "Distance: " + str(round(depth, 3)), (200, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                            (124, 252, 0), 2)
                # Multiply computer value with 205.8 to get real-life depth in [cm]. The factor was found manually.
            else:
                v2.putText(frame_right, "Diff Hand", (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame_left, "Diff Hand", (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        else:
            cv2.putText(frame_right, "TRACKING LOST", (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.putText(frame_left, "TRACKING LOST", (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)




        # Show the frames
        cv2.imshow("frame right", frame_right)
        cv2.imshow("frame left", frame_left)


        # Hit "q" to close the window
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


# Release and destroy all windows before termination
cap_right.release()
cap_left.release()

cv2.destroyAllWindows()
# Main program loop with face detector and depth estimation using stereo vision