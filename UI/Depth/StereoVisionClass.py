import cv2
from cvzone.HandTrackingModule import HandDetector
import pandas as pd
# Function for frame calibration
import Depth.calibration as calib
# Function for stereo vision and depth estimation
import Depth.triangulation as tri
# Mediapipe for face detection
import mediapipe as mp


class Stereo_Vision (object):

    def __init__(self, camera_left):

        self.hand_detection_left = HandDetector(detectionCon=0.8, maxHands=2) #Pasar por parametro desde la ui
        self.mp_draw = mp.solutions.drawing_utils #Ver que hace esto
        self.cap_left = cv2.VideoCapture(camera_left)
        #Leer del archivo
        confi_params = pd.read_csv('./Depth/confi.csv')
        self.frame_rate = int(confi_params[confi_params['depth_param'] == 'frame_rate'].value) # Camera frame rate (maximum at 120 fps)
        self.B = float(confi_params[confi_params['depth_param'] == 'B'].value) # Distance between the cameras [cm]
        self.f = float(confi_params[confi_params['depth_param'] == 'f'].value) # Camera lense's focal length [mm]
        self.alpha = float(confi_params[confi_params['depth_param'] == 'alpha'].value)


    def calculate_distances(self, frame_right, hand_right, ret_right):
        i = 0

        ret_left, frame_left = self.cap_left.read()

        ################## CALIBRATION #########################################################

        frame_right, frame_left = calib.undistorted(frame_right, frame_left)

        ########################################################################################

        # If cannot catch any frame, return
        if not ret_right or not ret_left:
            return -1

        else:

            # APPLYING SHAPE RECOGNITION:
            hand_left, frame_left = self.hand_detection_left.findHands(frame_left)

            # Hough Transforms can be used aswell or some neural network to do object detection
            if hand_right and hand_left:
            ################## CALCULATING HAND DEPTH #########################################################
                if hand_right[0]["type"] != hand_left[0]["type"] and len(hand_left) > 1:
                    i = 1  #Priorizamos derecha?

            # If no ball can be caught in one camera show text "TRACKING LOST"
                # Nos quedamos con la misma mano

                if hand_right[0]["type"] == hand_left[i]["type"]:

                    # Function to calculate depth of object. Outputs vector of all depths in case of several balls.
                    # All formulas used to find depth is in video presentaion
                    depth = tri.find_depth(hand_right[0]["center"], hand_left[i]["center"], frame_right, frame_left,
                                           self.B, self.f, self.alpha)
                    return depth

                else:
                    return -1 #Manos distintas

            else:
                return -1 #no trackea nada



