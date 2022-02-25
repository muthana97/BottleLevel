#Importing the libraries for use 
import numpy as np
import cv2
import time
import tkinter as tk


#Set up GUI
window = tk.Tk()  #Makes main window
window.wm_title("Vision inspection")
window.config(background="#FFFFFF")

 
global pp2mm #((pixel 2 mmm))
#Details Frame
Detailsframe = tk.Frame(window, width=350)
Detailsframe.grid(row=0, column=0, padx=5, pady=5)

#Graphics window
imageFrame = tk.Frame(window, width=350, height=350)
imageFrame.grid(row=0, column=1, padx=5, pady=5)

#Capture video frames
lmuthana = tk.Label(imageFrame)
lmuthana.grid(row=0, column=0)
cap = cv2.VideoCapture(0)

#MuthanaCode####################################################################


def muthana():
#Declare global variable pp2mm
    global pp2mm

#read camera frame
    _, frame = cap.read()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #convert to grayscale
    y = int(frame.shape[0])
    x = int(frame.shape[1])
    x1 = int((x / 2) - (x / 5.5))
    x2 = int((x / 2) + (x / 5.5))
    y1 = int((y / 2) + (y / 2.5))
    y2 = int((y / 2) - (y / 2.5))

#Line up the frame for region of detection
    cv2.line(frame, (x1, y1), (x2, y1), (255, 0, 0), 3)
    # cv2.line(frame, (x1, y2), (x2, y2), (255, 0, 0), 3)
    cv2.line(frame, (x1, y1), (x1, y2), (255, 0, 0), 3)
    cv2.line(frame, (x2, y1), (x2, y2), (255, 0, 0), 3)

#adjustments to measurements
    yy = int((y1 - y2) / 4)
    xx1 = int(x / 2 - (x / 18))
    xx2 = int(x / 2 + (x / 18))

#Define region of interest
    ROI = img[yy:(y1), xx1:(xx2 - 1)]
    edges = cv2.Canny(ROI, 70, 80)  # Detect edges(with set thresholds)#Detect Edges
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 30, maxLineGap=120) #Detect lines
    #cv2.imshow('edges', edges)


#Draw the detected liquid level line
    line = lines[0]
    x11, y11, x22, y22 = line[0]
    y11 = int(y11 + yy)
    x11 = x11 + x1
    x22 = x22 + x2
    cv2.line(frame, (x11, y11), (x22, y11), (0, 255, 0), 3)

#Find height of liquid inside bottle in units of "mm"	
    s=int(abs(y11-y1))
    pp2mm=(s*25.4)/96
    cv2.putText(frame, str(pp2mm),(x22,y11), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,0,255), lineType=cv2.LINE_AA)

#Introduces a delay
    time.sleep(0.09)

#Resize video frame (for the GUI)
    width = 350
    height = 350
    dim = (width, height)
    resized = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    img = Image.fromarray(resized)
    imgtk = Image.PhotoImage(image=img)
    lmuthana.imgtk = imgtk
    lmuthana.configure(image=imgtk)
    lmuthana.after(10, muthana)
    mmLabel = tk.Label(Detailsframe, text=("Measurement: " + str(round(pp2mm)) + "mm"))
    mmLabel.grid(row=0, column=0, padx=0, pady=0)

#Check if the liquid level PASS

    if pp2mm>80:
       LevelLabel = tk.Label(Detailsframe, text="Pass")
       LevelLabel.grid(row=0, column=1, padx=0,pady=2)
    elif pp2mm<80:
       LevelLabel = tk.Label(Detailsframe, text="fail")
       LevelLabel.grid(row=0, column=1, padx=0,pady=2)
    	#cv2.imshow("Detected Level!", frame)
    	#cv2.imshow("noise", edges)
#################################################################################

muthana()


window.mainloop()