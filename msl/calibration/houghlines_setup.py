from Tkinter import *
import numpy as np
import cv2
import time
import imutils
# import sys
import platform
import cPickle as pickle

class HoughlineCalibrator:

	def __init__(self, hougline_params_initial={'canny_threshold1': 50,'canny_threshold2': 150,
									'canny_apertureSize': 3,'rho': 1,'theta': 180,'threshold': 200}):

		self.window_name = 'Set Houghlines Parameters'
		self.params = hougline_params_initial
		self.clean_image = None

		if platform.system() == 'Linux':
			from picamera.array import PiRGBArray
			from picamera import PiCamera
			
			self.camera = PiCamera()
			self.camera.resolution = (1120, 630)
			self.rawCapture = PiRGBArray(self.camera, size=(1120, 630))

		else:
			self.camera = cv2.VideoCapture(0)

		time.sleep(0.25)

		self.build_sliders()

	def build_sliders(self):

		self.master = Tk()
		self.master.wm_title(self.window_name)

		canny_threshold1_label = Label(self.master, text="canny_threshold1")
		canny_threshold1_label.pack()
		self.canny_threshold1 = Scale(self.master, from_=1, to=400, orient=HORIZONTAL)
		self.canny_threshold1.set(self.params['canny_threshold1'])
		self.canny_threshold1.pack()

		canny_threshold2_label = Label(self.master, text="canny_threshold2")
		canny_threshold2_label.pack()
		self.canny_threshold2 = Scale(self.master, from_=1, to=400, orient=HORIZONTAL)
		self.canny_threshold2.set(self.params['canny_threshold2'])
		self.canny_threshold2.pack()

		canny_apertureSize_label = Label(self.master, text="canny_apertureSize")
		canny_apertureSize_label.pack()
		self.canny_apertureSize = Scale(self.master, from_=2, to=3, orient=HORIZONTAL)
		self.canny_apertureSize.set((self.params['canny_apertureSize']+1)/2)
		self.canny_apertureSize.pack()

		rho_label = Label(self.master, text="rho")
		rho_label.pack()
		self.rho = Scale(self.master, from_=1, to=10, orient=HORIZONTAL)
		self.rho.set(self.params['rho'])
		self.rho.pack()

		theta_label = Label(self.master, text="x (theta=pi/x)")
		theta_label.pack()
		self.theta = Scale(self.master, from_=1, to=360, orient=HORIZONTAL)
		self.theta.set(self.params['theta'])
		self.theta.pack()

		threshold_label = Label(self.master, text="threshold")
		threshold_label.pack()
		self.threshold = Scale(self.master, from_=0, to=800, orient=HORIZONTAL)
		self.threshold.set(self.params['threshold'])
		self.threshold.pack()

		done = Button(self.master, text="Next", command=self.finish)
		done.pack()

	def next_frame(self):

		if platform.system() == 'Linux':
			self.camera.capture(self.rawCapture, format="bgr")
			self.clean_image = rawCapture.array
		else:
			(grabbed, self.clean_image) = self.camera.read()
			if not grabbed:
				raise Exception('Could not read from camera.')

	def task(self):
		self.next_frame()

		gray = cv2.cvtColor(self.clean_image, cv2.COLOR_BGR2GRAY)
		edges = cv2.Canny(gray,
					self.canny_threshold1.get(),
					self.canny_threshold2.get(),
					apertureSize = ((self.canny_apertureSize.get()*2) - 1)
				)

		lines = cv2.HoughLines(edges,
						self.rho.get(),
						np.pi/self.theta.get(),
						self.threshold.get()
					)
		if lines != None:
				for line in lines:
						rho_x,theta_x = line[0]
						a = np.cos(theta_x)
						b = np.sin(theta_x)
						x0 = a*rho_x
						y0 = b*rho_x
						x1 = int(x0 + 1000*(-b))
						y1 = int(y0 + 1000*(a))
						x2 = int(x0 - 1000*(-b))
						y2 = int(y0 - 1000*(a))

						cv2.line(self.clean_image,(x1,y1),(x2,y2),(0,0,255),2)
		
		self.clean_image = imutils.resize(self.clean_image, width=1000)
		cv2.imshow(self.window_name, self.clean_image)

		self.master.after(20, self.task)

	def start(self):

		self.master.after(20, self.task)
		self.master.mainloop()

	def finish(self):

		self.params = {
			'canny_threshold1': self.canny_threshold1.get(),
			'canny_threshold2': self.canny_threshold2.get(),
			'canny_apertureSize': ((self.canny_apertureSize.get()*2) - 1),
			'rho': self.rho.get(),
			'theta': self.theta.get(),
			'threshold': self.threshold.get()
			}	

		cv2.destroyWindow(self.window_name)
		self.master.destroy()

	def calibrate(self):

		self.start()
		return self.params

# hc = HoughlineCalibrator().calibrate()
# print hc





