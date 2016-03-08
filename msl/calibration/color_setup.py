from Tkinter import *
import numpy as np
import cv2
import time
import imutils
import platform
# import sys
import cPickle as pickle

class ColorCalibrator:

	def __init__(self, color, color_params_initial={'b1': 0,'g1': 0,'r1': 0,'b2': 255,'g2': 255,'r2': 255}):

		self.color = color
		self.window_name = "Set " + self.color + " Ranges"

		self.image = None
		if platform.system() == 'Linux':
		    from picamera.array import PiRGBArray
		    from picamera import PiCamera
		    
		    camera = PiCamera()
		    time.sleep(0.25)
		    camera.resolution = (1120, 630)
		    rawCapture = PiRGBArray(camera, size=(1120, 630))

		    camera.capture(rawCapture, format="bgr")
		    self.image = rawCapture.array
		else:
		    camera = cv2.VideoCapture(0)
		    time.sleep(0.25)
		    (grabbed, image) = camera.read()
		    if not grabbed:
		    	raise Exception('Couldn\'t grab snapshot.' )
		    self.image = image

		self.params = color_params_initial
		self.build_sliders()

	def build_sliders(self):

		self.master = Tk()
		self.master.wm_title(self.window_name)

		b1_label = Label(self.master, text="Blue Low")
		b1_label.pack()
		self.b1 = Scale(self.master, from_=0, to=255, orient=HORIZONTAL)
		self.b1.set(self.params['b1'])
		self.b1.pack()
		b2_label = Label(self.master, text="Blue High")
		b2_label.pack()
		self.b2 = Scale(self.master, from_=0, to=255, orient=HORIZONTAL)
		self.b2.set(self.params['b2'])
		self.b2.pack()

		g1_label = Label(self.master, text="Green Low")
		g1_label.pack()
		self.g1 = Scale(self.master, from_=0, to=255, orient=HORIZONTAL)
		self.g1.set(self.params['g1'])
		self.g1.pack()
		g2_label = Label(self.master, text="Green High")
		g2_label.pack()
		self.g2 = Scale(self.master, from_=0, to=255, orient=HORIZONTAL)
		self.g2.set(self.params['g2'])
		self.g2.pack()

		r1_label = Label(self.master, text="Red Low")
		r1_label.pack()
		self.r1 = Scale(self.master, from_=0, to=255, orient=HORIZONTAL)
		self.r1.set(self.params['r1'])
		self.r1.pack()
		r2_label = Label(self.master, text="Red High")
		r2_label.pack()
		self.r2 = Scale(self.master, from_=0, to=255, orient=HORIZONTAL)
		self.r2.set(self.params['r2'])
		self.r2.pack()

		done = Button(self.master, text="Next", command=self.finish)
		done.pack()

	def task(self):

		lower = np.array([self.b1.get(), self.g1.get(), self.r1.get()], dtype = "uint8")
		upper = np.array([self.b2.get(), self.g2.get(), self.r2.get()], dtype = "uint8")
		mask = cv2.inRange(self.image, lower, upper)
		output = cv2.bitwise_and(self.image, self.image, mask = mask)
		cv2.imshow(self.window_name, output)
		self.master.after(20, self.task)

	def start(self):

		self.master.after(20, self.task)
		self.master.mainloop()

	def finish(self):

		self.params = {
			'b1': self.b1.get(),
			'g1': self.g1.get(),
			'r1': self.r1.get(),
			'b2': self.b2.get(),
			'g2': self.g2.get(),
			'r2': self.r2.get()
			}	

		cv2.destroyWindow(self.window_name)
		self.master.destroy()

	def calibrate(self):

		self.start()
		return self.params













