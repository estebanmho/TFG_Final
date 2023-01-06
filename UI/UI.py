import os
import tkinter
from Depth.calibration_images import *
from Depth.stereo_calibration import *
from Prediction.PredictiveClass import *
import traceback
import logging

camera_one_value = 0

def hide_camera_two():
    try:
        if checked_state.get() == 1:
            camera_two.grid(row=2, column=1, padx=10, pady=10)
            camera_two_label.grid(row=2, column=0, padx=10, pady=10)
        else:
            camera_two.grid_remove()
            camera_two_label.grid_remove()
    except Exception as e:
        tkinter.messagebox.showinfo("Log", traceback.format_exc())
        window.deiconify()



def start_program():
    window.withdraw()
    tkinter.messagebox.showinfo("Instructions", "Press q to stop tracking.")
    execution = PredictiveClass(int(camera_one.get()))
    if checked_state.get() == 1:
        execution.include_depth(int(camera_two.get()))
    try:
        execution.main_function()
        window.destroy()
    except Exception as e:
        tkinter.messagebox.showinfo("Instructions", "Camara not detected or not compatible.")
        tkinter.messagebox.showinfo("Log", traceback.format_exc())
        window.deiconify()


def calibrate():
    try:
        window.withdraw()
        if checked_state.get() == 1:
            if int(camera_one.get()) == int(camera_two.get()):
                tkinter.messagebox.showinfo("Instructions", "Same camera selected.")
            else:
                var_cal = CalibrationImages(int(camera_one.get()), int(camera_two.get()))
                var_cal.start_calibration()
                stereo_calibrate()
                tkinter.messagebox.showinfo("Instructions", "The cameras has been calibrated.")
        else:
            tkinter.messagebox.showinfo("Instructions", "No second camera configurated.")
        window.deiconify()
    except Exception as e:
        tkinter.messagebox.showinfo("Log", traceback.format_exc())
        window.deiconify()



window = tkinter.Tk()
window.title("Hand - Mouse")
window.configure(bg="#F8EDE3")

title_label = tkinter.Label(text="Control the PC", font=("Arial", 38), fg="#7D6E83", bg="#F8EDE3")
title_label.grid(row=0, column=1, padx=20, pady=20)

camera_one_label = tkinter.Label(text="Camera One", font=("Arial", 12), fg="#7D6E83", bg="#F8EDE3")
camera_one_label.grid(row=1, column=0, padx=10, pady=10)
camera_one = tkinter.Spinbox(width=5, from_=0, to=256)
camera_one.grid(row=1, column=1, padx=10, pady=10)

camera_two_label = tkinter.Label(text="Camera Two", font=("Arial", 12), fg="#7D6E83", bg="#F8EDE3")
camera_two = tkinter.Spinbox(width=5, from_=0, to=256)


checked_state = tkinter.IntVar()
stereo_on = tkinter.Checkbutton(text="Stereo cam", variable=checked_state, font=("Arial", 12), fg="#7D6E83", bg="#F8EDE3", command=hide_camera_two)
stereo_on.grid(row=3, column=1, padx=10, pady=10)


start_button = tkinter.Button(fg="#F8EDE3", bg="#D0B8A8", text="Start Control", command=start_program)
start_button.grid(row=4, column=1, padx=10, pady=10)

start_button = tkinter.Button(fg="#F8EDE3", bg="#D0B8A8", text="Stereo Calibration", command=calibrate)
start_button.grid(row=4, column=3, padx=10, pady=10)

window.mainloop()