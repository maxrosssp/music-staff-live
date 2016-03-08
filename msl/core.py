import datetime
import imutils
import time
import cv2
import platform
import sys
from msl.parameters.operator import ParamOperator
from msl.sight.staff import Staffer
from msl.sound import Player
import os

class MSLive:

	def __init__(self, tempo=80, camera=cv2.VideoCapture(0), 
						motion_count_start=20, motion_threshold=25, motion_min_area=500,
						diff_count_start=600, diff_threshold=40, diff_min_area=18000):
		
		self.param_operator = ParamOperator()
		# self.CIRCLE_PARAMS = self.param_operator.load('CIRCLE_PARAMS')
		self.HOUGHLINES_PARAMS = self.param_operator.load('HOUGHLINES_PARAMS')
		self.BLUE_PARAMS = self.param_operator.load('BLUE_PARAMS')
		self.PINK_PARAMS = self.param_operator.load('PINK_PARAMS')
		self.tempo = tempo

		self.motion_count_start = motion_count_start
		self.motion_threshold = motion_threshold
		self.motion_min_area = motion_min_area

		self.diff_count_start = diff_count_start
		self.diff_threshold = diff_threshold
		self.diff_min_area = diff_min_area

		self.camera = camera
		time.sleep(0.25)

		self.motion_count = self.motion_count_start
		self.diff_count = self.diff_count_start

		self.frame_count = 0

		self.motion = False
		self.motion_detected = False
		self.create_song = False

		self.setup_frames()

	def move_to_next_frame(self):
		self.frame_count += 1
		(grabbed, frame) = self.camera.read()
		if not grabbed:
			raise Exception('Could not read next frame from camera!')
		self.currentFrame = frame
		self.currentFrameGray = cv2.GaussianBlur(cv2.cvtColor(self.currentFrame, cv2.COLOR_BGR2GRAY), (21, 21), 0)

	def setup_frames(self):
		self.move_to_next_frame()
		self.previousFrame = self.currentFrameGray
		self.compareFrame = self.previousFrame
		self.previous2frames = [self.currentFrameGray, self.currentFrameGray]

	def detect_change(self, frameGray, compareFrame, threshold, min_area):

		frameDelta = cv2.absdiff(compareFrame, frameGray)
		thresh = cv2.threshold(frameDelta, threshold, 255, cv2.THRESH_BINARY)[1]
		thresh = cv2.dilate(thresh, None, iterations=2)
		(_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)

		for c in cnts:
			if cv2.contourArea(c) < min_area:
				continue
			return True, frameDelta

		return False, frameDelta

	def detect_motion(self, frameGray, previousFrame):

		return self.detect_change(frameGray, previousFrame, self.motion_threshold, self.motion_min_area)

	def detect_diff(self, frameGray, compareFrame):

		return self.detect_change(frameGray, compareFrame, self.diff_threshold, self.diff_min_area)

	def detect_input(self):
		grabbed, self.currentFrame = self.grab_next_frame()
		self.currentFrameGray = cv2.GaussianBlur(cv2.cvtColor(self.currentFrame, cv2.COLOR_BGR2GRAY), (21, 21), 0)

	def update(self):
		self.move_to_next_frame()

		if self.frame_count == 10:
			self.previous2frames.insert(0, self.currentFrameGray)
			self.previous2frames.pop()
			self.frame_count = 0

		diff_detected, diff_frameDelta = self.detect_diff(self.currentFrameGray, self.compareFrame)
		self.motion_detected, motion_frameDelta = self.detect_motion(self.currentFrameGray, self.previousFrame)
		if self.motion:
			if self.motion_detected:
				self.motion_count = self.motion_count_start
			else:
				self.motion_count -= 1
				if self.motion_count <= 0:
					print "Motion count down complete"
					if not diff_detected:
						print "Diff not detected. Go to play sound."
						self.motion_count = self.motion_count_start
						self.motion = False
					else:
						self.diff_count -= 1
						if self.diff_count == 0:
							print "Diff countdown complete. Resetting frame."
							self.diff_count = self.diff_count_start
							self.motion_count = self.motion_count_start
							self.motion = False
							self.create_song = False
		else:
			if self.motion_detected:
				print "MOTION DETECTED"
				self.motion = True
				self.create_song = True
				self.compareFrame = self.previous2frames[1]

		self.previousFrame = self.currentFrameGray
				

	def render(self):
		if (not self.motion) and (not self.motion_detected) and self.create_song:
			print "Do stuff"

			frame = self.currentFrame

			staffer = None
			get_staff = True
			while get_staff:
				try:
					print "Try to create staff."
					get_staff = False
					staffer = Staffer(frame,
								tempo=self.tempo,
					            CANNY_THRESHOLD1=self.HOUGHLINES_PARAMS['canny_threshold1'], 
					            CANNY_THRESHOLD2=self.HOUGHLINES_PARAMS['canny_threshold2'], 
					            CANNY_APERTURESIZE=self.HOUGHLINES_PARAMS['canny_apertureSize'], 
					            RHO=self.HOUGHLINES_PARAMS['rho'], 
					            THETA=self.HOUGHLINES_PARAMS['theta'], 
					            THRESHOLD=self.HOUGHLINES_PARAMS['threshold'],
					            DP=self.CIRCLE_PARAMS['dp'], 
					            MINDIST=self.CIRCLE_PARAMS['minDist'], 
					            PARAM1=self.CIRCLE_PARAMS['param1'], 
					            PARAM2=self.CIRCLE_PARAMS['param2'], 
					            MINRADIUS=self.CIRCLE_PARAMS['minRadius'], 
					            MAXRADIUS=self.CIRCLE_PARAMS['maxRadius'],
					            BLUE_B1 = self.BLUE_COLOR_PARAMS['b1'],
				                BLUE_G1 = self.BLUE_COLOR_PARAMS['g1'],
				                BLUE_R1 = self.BLUE_COLOR_PARAMS['r1'],
				                BLUE_B2 = self.BLUE_COLOR_PARAMS['b2'],
				                BLUE_G2 = self.BLUE_COLOR_PARAMS['g2'],
				                BLUE_R2 = self.BLUE_COLOR_PARAMS['r2'],
				                PINK_B1 = self.PINK_COLOR_PARAMS['b1'],
				                PINK_G1 = self.PINK_COLOR_PARAMS['g1'],
				                PINK_R1 = self.PINK_COLOR_PARAMS['r1'],
				                PINK_B2 = self.PINK_COLOR_PARAMS['b2'],
				                PINK_G2 = self.PINK_COLOR_PARAMS['g2'], 
				                PINK_R2 = self.PINK_COLOR_PARAMS['r2']
					        )
					staffer.export_wav("final.wav")
					player = Player()
					player.play_file("final.wav")
					player.terminate()
				except:
					print "Couldn't create staff."
					(grabbed, frame) = self.camera.read()
					while not grabbed:
						(grabbed, frame) = self.camera.read()
					get_staff = True

			self.create_song = False

	def start(self, calibrate=False):

		if calibrate:
			from msl.calibration.calibrators import *

			self.BLUE_PARAMS = ColorCalibrator('Blue', self.BLUE_PARAMS).calibrate()
			self.param_operator.dump('BLUE_PARAMS', self.BLUE_PARAMS)
			self.PINK_PARAMS = ColorCalibrator('Pink', self.PINK_PARAMS).calibrate()
			self.param_operator.dump('PINK_PARAMS', self.PINK_PARAMS)
			self.HOUGHLINES_PARAMS = HoughlineCalibrator(self.HOUGHLINES_PARAMS).calibrate()
			self.param_operator.dump('HOUGHLINES_PARAMS', self.HOUGHLINES_PARAMS)

			time.sleep(3)

		while True:
			self.update()

			key = cv2.waitKey(1)
			if key == ord("q"):
				break

			self.render()






