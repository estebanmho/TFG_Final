import cv2
import tkinter.messagebox


class CalibrationImages:

    def __init__(self, camera_one, camera_two):
        self.cap = cv2.VideoCapture(camera_one)
        self.cap2 = cv2.VideoCapture(camera_two)

        self.num = 0

    def start_calibration(self):
        tkinter.messagebox.showinfo("Instructions", "Press s to take a photo, q to quit")

        while self.cap.isOpened():

            succes1, img = self.cap.read()
            succes2, img2 = self.cap2.read()


            k = cv2.waitKey(5)


            if k == ord('s'): # wait for 's' key to save and exit
                cv2.imwrite('./Depth/images/stereoLeft/imageL' + str(self.num) + '.png', img)
                cv2.imwrite('./Depth/images/stereoRight/imageR' + str(self.num) + '.png', img2)
                print("images saved!")
                self.num += 1

            elif k == ord('q'):
                cv2.destroyAllWindows()
                break

            cv2.imshow('Img 1',img)
            cv2.imshow('Img 2',img2)

