"""Emily Yeh and Lydia Zuehsow"""

"""This program allows a person to wave a flashlight or laser pointer to cast spells, Harry Potter-style!"""

"""For future reference, here's a link to our Google doc: https://docs.google.com/document/d/1daGjz8CWycfev0Fs96ru-Na5JNtqs2nVE1fHZ1ydhX0/edit?usp=sharing"""


from collections import deque
import cv2
import imutils
import os, sys
import argparse
import pygame
from pygame.locals import *
import time
import numpy as np
import random


class WebCam(object):
	def __init__(self, bufsize = 100, counter = 0):
		"""Run webcam, find green, return center coordinates?"""
		self.camera = cv2.VideoCapture(0)
		#construct argument parse, parse arguments
		self.ap = argparse.ArgumentParser()
		self.ap.add_argument("-v","--video",
			help="path to the(optional) video file")
		self.bufsize = bufsize
		self.ap.add_argument("-b", "--buffer", type=int, default = 100,
			help="max buffer size")
		self.pts = deque(maxlen=bufsize)
		self.rad = []
		self.counter = counter
		self.calpts = deque(maxlen=bufsize)
		self.calrad = []
		self.calcounter = counter

	def getcenter(self, greenLower, greenUpper):
		self.args = vars(self.ap.parse_args())

		#initialize tracked points, frame counter, coordinate deltas

		#grab current frame
		(self.grabbed, self.frame) = self.camera.read()
		
		#resize frame, blur frame, conert to HSV color space
		self.frame = imutils.resize(self.frame, width=600)
		blurred = cv2.GaussianBlur(self.frame,(11,11),0)
		hsv = cv2.cvtColor(self.frame,cv2.COLOR_BGR2HSV)

		#construct mask for "green", perform dilations and erosions
		#to remove erroneous parts of mask
		mask = cv2.inRange(hsv, greenLower, greenUpper)
		mask = cv2.erode(mask,None,iterations=1)
		mask = cv2.dilate(mask,None,iterations=1)

		#find contours in the mask, initialize current (x,y) center
		self.cnts = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)[-2]

		#only continue if at least one contour is found
		if len(self.cnts) > 0:

			#find largest contour in mask, use it to compute 
			#minimum enclosing circle and centroid for that contour

			c = max(self.cnts,key=cv2.contourArea)
			M = cv2.moments(c)
			(center,radius) = cv2.minEnclosingCircle(c)
			Mlist= [M["m10"], M["m00"],M["m01"],M["m00"]]
			if any(Mlist) == 0:
				return None
			else:
				center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
				return [center,radius]

	def update_webcam(self, center):
		cv2.circle(webcam.frame,center,5,redColor, -1)

		cv2.line(webcam.frame, (0,0), (0,450), redColor, 1)
		cv2.line(webcam.frame, (200,0), (200,450), redColor, 1)
		cv2.line(webcam.frame, (400,0), (400,450), redColor, 1)
		cv2.line(webcam.frame, (600,0), (600,450), redColor, 1)

		cv2.line(webcam.frame, (0,0), (600,0), redColor, 1)
		cv2.line(webcam.frame, (0,150), (600,150), redColor, 1)
		cv2.line(webcam.frame, (0,300), (600,300), redColor, 1)

	def process_pts(self, caldx, caldy):
		dsX=0
		dsY=0
		dX = self.pts[i-buf][0] - webcam.pts[i][0]
		dY = self.pts[i-buf][1] - webcam.pts[i][1]

class Calibration(object):
	"""Performs calibration of the 'green thing' and represents the calibrated original "green object" """
	def __init__(self):
		self=self
	def startup(self,greenLower,greenUpper):
		calibrating = True
		count = 0
		calradi = 0
		caldx = 0
		caldy = 0
		calx = 0
		caly = 0
		caldXs=[]
		caldYs=[]
		calxs=[]
		calys=[]
		while calibrating:
			califind = webcam.getcenter(greenLower, greenUpper)
			A = "Please hold your object very still"
			B =	"in the center of the screen."
			C = "The system is calibrating."
			D = "This will only take a moment."
			cv2.putText(webcam.frame,A,(10,30),cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,0,255),3)
			cv2.putText(webcam.frame,B,(10,100),cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,0,255),3)
			cv2.putText(webcam.frame,C,(10,170),cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,0,255),3)
			cv2.putText(webcam.frame,D,(10,240),cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,0,255),3)
			if califind != None:
				calicenter = califind[0]
				caliradius = califind[1]

				if caliradius > 20:
				#if radius is above a certain size we count it
					webcam.calpts.append(calicenter)
					webcam.calrad.append(caliradius)
					webcam.calcounter = webcam.calcounter + 1
					calcounter = webcam.calcounter

			buf = 10
			for i in range (1,len(webcam.calpts)):
			# ignoring tracked points that are None
				if webcam.calpts[i-1] is None or webcam.calpts[i] is None:
					pass
			#making sure we have enough points
				if webcam.calcounter >= buf and webcam.calpts[i-buf] is not None:
					#compute difference between x and y coordinates of the point and the point
					#minimum buffer length before it
					count = count + 1
					calx= webcam.calpts[i][0]
					caly= webcam.calpts[i][1]
					caldX = webcam.calpts[i-buf][0] - webcam.calpts[i][0]
					caldY = webcam.calpts[i-buf][1] - webcam.calpts[i][1]
					caldXs.append(caldX)
					caldYs.append(caldY)
					calxs.append(calx)
					calys.append(caly)
			cv2.imshow("Frame",webcam.frame)
			key = cv2.waitKey(1) & 0xFF

			#Eliminates accidental infinity loops by setting a frame limit on runtime.

			if count > 30:
				calradi = np.mean(webcam.calrad)
				caldx = np.mean(caldXs)
				caldy = np.mean(caldYs)
				calx = np.mean(calxs)
				caly = np.mean(calys)
				return [calradi, (caldx,caldy),(calx,caly)]
				running = False


class Mouse(object):
	"""Represents your spell trail"""
	def __init__(self,color,x=50,y=50,selected=False):
		self.x = x
		self.y = y
		self.color = color
		self.selected = selected

	def set_pos(self, x, y):
		self.x = x
		self.y = y
		# self.color = redColor

	def Move(self):
		gotcenter = webcam.getcenter(greenLower, greenUpper)
		if gotcenter == None:
			pass
		else:
			center = gotcenter[0]
			self.x = center[0]
			self.y = center[1]
		self.set_pos(self.x, self.y)

class Enemy(object):
	"""Represents your opponent"""
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.hp = 100
	def Move(self, newx, newy):
		self.x = newx
		self.y = newy
	def DamageTaken(self,dmg):
		self.hp = self.hp - dmg


class DesktopModel(object):
	"""Stores the fake desktop state"""
	def __init__(self):
		# self.desktop = screen.fill(whiteColor)
		# pygame.display.update()

		self.grid1flag = False
		self.grid2flag = False
		self.grid3flag = False
		self.grid4flag = False
		self.grid5flag = False
		self.grid6flag = False
		self.grid7flag = False
		self.grid8flag = False
		self.grid9flag = False

	def spell_check(self):
		if self.grid1flag and self.grid4flag and self.grid7flag and self.grid8flag and self.grid9flag and self.grid6flag and self.grid3flag and (self.grid2flag == False) and (self.grid5flag == False) and (spell_frame <= 10):
			if spell_frame == 1:
				print 'Incendio!'
				enemy.hp = enemy.hp - 50
			return True

		elif self.grid2flag and self.grid5flag and self.grid8flag and self.grid1flag == False and self.grid3flag == False and self.grid4flag == False and self.grid6flag == False and self.grid7flag == False and self.grid9flag == False and (spell_frame <= 10):
			print 'Wingardium leviosa!'
			return True

		elif self.grid1flag and self.grid4flag and self.grid7flag and self.grid2flag == False and self.grid3flag == False and self.grid5flag == False and self.grid6flag == False and self.grid8flag == False and self.grid9flag == False and (spell_frame <= 10):
			if spell_frame == 1:
				print 'Flipendo!'
				enemy.hp = enemy.hp - 25
			return True

		elif self.grid2flag and self.grid5flag and self.grid4flag and self.grid8flag and self.grid6flag and self.grid1flag == False and self.grid3flag == False and self.grid7flag == False and self.grid9flag == False and (spell_frame <= 10):
			print 'Avada kedavra!'
			# Gameover screen
			return True

		elif self.grid1flag and self.grid4flag and self.grid5flag and self.grid6flag and self.grid9flag and self.grid2flag == False and self.grid3flag == False and self.grid7flag == False and self.grid8flag == False and (spell_frame <= 10):
			print 'Stupefy!'
			# Gameover screen
			return True

		elif self.grid1flag and self.grid4flag and self.grid7flag and self.grid5flag and self.grid3flag and self.grid6flag and self.grid9flag and self.grid2flag == False and self.grid8flag == False and (spell_frame <= 10):
			print 'Expelliarmus!'
			# Gameover screen
			return True

		else:
			return False

	def spell_clear(self):
		model.grid1flag = False
		model.grid2flag = False
		model.grid3flag = False
		model.grid4flag = False
		model.grid5flag = False
		model.grid6flag = False
		model.grid7flag = False
		model.grid8flag = False
		model.grid9flag = False

class PygameView(object):
	"""Visualizes a fake desktop in a pygame window"""
	def __init__(self,model,screen,background, sprite, explosion):
		"""Initialise the view with a specific model"""
		self.model = model
		self.screen = screen.fill(whiteColor)

		# Load background png and post to screen
		background = pygame.image.load(background).convert()
		background = pygame.transform.scale(background, (screenwidth,screenheight))
		screen.blit(background,(0,0))

		# Load enemy sprite png
		self.sprite = pygame.image.load(sprite).convert_alpha()

		# Load spell damage animation png
		self.explosion = pygame.image.load(explosion).convert_alpha()
		self.explosion = pygame.transform.scale(self.explosion, (250,250))

		# Enemy HP bar
		screen.fill((0,255,0),Rect(10,10,100,20))

		# Update game display
		pygame.display.update()

	def update(self):
		"""Draw the game state to the screen"""
		print enemy.hp

		# Enemy spell damage animation
		if model.spell_check() and (spell_frame <= 10):
			screen.blit(self.explosion,(enemy.x + 200,enemy.y + 150))
		else:
			screen.blit(self.sprite,(enemy.x,enemy.y))

		# Enemy HP bar
		if model.spell_check() and (spell_frame == 1):
			screen.fill((255,0,0),Rect(10,10,(100 - enemy.hp),20))

		# pygame.draw.circle(screen,cursor.color,(int(cursor.x),int(cursor.y)),20,0)
		pygame.display.update()


class Controller(object):
	def __init__(self,model):
		self.model = model
	def process_events(self):
 		"""Process all of the events in the queue"""
 		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			elif event.type == GRID:
				if x <= 200 and y <= 150:
					# print 'Grid 1'
					model.grid1flag = True
				if (x >= 200 and x <= 400) and y <=150:
					# print 'Grid 2'
					model.grid2flag = True
				if x >= 400 and y <= 150:
					# print 'Grid 3'
					model.grid3flag = True
				if x <= 200 and (y >= 150 and y <=300):
					# print 'Grid 4'
					model.grid4flag = True
				if (x >= 200 and x <= 400) and (y >= 150 and y <=300):
					# print 'Grid 5'
					model.grid5flag = True
				if x >= 400 and (y >= 150 and y <= 300):
					# print 'Grid 6'
					model.grid6flag = True
				if x <= 200 and y >= 300:
					# print 'Grid 7'
					model.grid7flag = True
				if (x >= 200 and x <= 400) and y >= 300:
					# print 'Grid 8'
					model.grid8flag = True
				if x >= 400 and y >= 300:
					# print 'Grid 9'
					model.grid9flag = True

		pygame.event.clear()


if __name__ == '__main__':

	"""Initializing"""

	# Initialize pygame
	pygame.init()

	# Define some colors
	redColor = pygame.Color(255,0,0)
	greenColor = pygame.Color(0,255,0)
	blueColor = pygame.Color(0,0,255)
	whiteColor = pygame.Color(255,255,255)

	# Set pygame fake desktop size
	screenwidth= 600
	screenheight= 450

	size = (screenwidth, screenheight)
	screen = pygame.display.set_mode(size)

	model = DesktopModel()
	view = PygameView(model, screen, 'forbiddenforest.jpeg', 'volde.png', 'flame.png')
	master = Controller(model)

	"""WEBCAM STUFF"""

	#initialize stuff

	running = True
	frame = 0
	eventcount = 0
	webcam = WebCam()

	greenLower= (29,86,6)
	greenUpper= (64,255,255)

	calibrate = Calibration()
	[calradi,(caldx,caldy),(calx,caly)] = calibrate.startup(greenLower,greenUpper)

	cursor = Mouse(blueColor,calx,caly,False)
	enemy = Enemy(25, 100)
	# cursor.initialsetup()

	center = 0
	calcounter = 0
	(dX,dY) = (0,0)
	dXs=[]
	dYs=[]
	(caldX,caldY)=(0,0)
	caldXs=[]
	caldYs=[]

	GRID = pygame.USEREVENT+2
	grid_event = pygame.event.Event(GRID)

	# makes sure only the events we want are on the event queue
	allowed_events = [QUIT,GRID]
	pygame.event.set_allowed(allowed_events)

	buf = 10
	# "buf" is the buffer- the number of frames we go backwards 
	# to compare for movement- so if buf is 10, we compare 
	# the location of the "green" in the current frame 
	# to its location 10 frames earlier. 
	

	"""RUNTIME LOOP"""

	# This is the main loop of the program. 
	spell_frame = 0

	while running:

		# Check for spells
		if model.spell_check(): #if a spell is detected, add one to spell frame count
			spell_frame += 1

		if spell_frame <= 10: #if a spell has finished firing, reset spell frame counter and clear all grid flags.
			pass
		else:
			model.spell_clear()
			spell_frame = 0

		# print model.store_flags

		# pygame.draw.circle(screen,ballcolor,(int(cursor.x),int(cursor.y)),20,0)
		#Find the center of any green objects' contours

		gotcenter = webcam.getcenter(greenLower, greenUpper)
		if gotcenter == None:
			pass
		else:
			center = gotcenter[0]
			radius = gotcenter[1]
			webcam.update_webcam(center)

			if radius > 20:
				#if radius is above a certain size we count it
				webcam.pts.append(center)
				webcam.rad.append(radius)
				webcam.counter = webcam.counter + 1

				(x,y) = center
				cursor.set_pos(x,y)
				# print (cursor.x,cursor.y)

				if (x >= 0 and x <= 600) and (y >= 0 and y <= 450):
					pygame.event.post(grid_event)

		for i in range (1,len(webcam.pts)):
			# ignoring tracked points that are None
			if webcam.pts[i-1] is None or webcam.pts[i] is None:
				pass
			#making sure we have enough points
			if webcam.counter >= buf and webcam.pts[i-buf] is not None:
				#compute difference between x and y coordinates of the point and the point
				#minimum buffer length before it
				webcam.process_pts(caldx,caldy)
			#process the events in the queue
			master.process_events()

		# Update the frames of the webcam video
		cv2.imshow("Frame",webcam.frame)
		key = cv2.waitKey(1) & 0xFF

		frame = frame + 1
		# Update the fake pygame desktop
		view.update()


		time.sleep(.001)
		if key == ord("q"):
			break
		if key == ord("c"):
			model.spell_clear()
		if frame > 500:
			pygame.quit
			sys.exit()
			break

if running == False:
		#release camera, close open windows
		webcam.camera.release()
		cv2.destroyAllWindows()


# print model.store_flags

	# def list_grids(self, store):
	# 	if x <= 200 and y <= 150:
	# 		current_grid = 1
	# 		if current_grid != store[-1]:
	# 			store.append(current_grid)
	# 	if (x >= 200 and x <= 400) and y <=150:
	# 		current_grid = 2
	# 		if current_grid != store[-1]:
	# 			store.append(current_grid)
	# 	if x >= 400 and y <= 150:
	# 		current_grid = 3
	# 		if current_grid != store[-1]:
	# 			store.append(current_grid)
	# 	if x <= 200 and (y >= 150 and y <=300):
	# 		current_grid = 4
	# 		if current_grid != store[-1]:
	# 			store.append(current_grid)
	# 	if (x >= 200 and x <= 400) and (y >= 150 and y <=300):
	# 		current_grid = 5
	# 		if current_grid != store[-1]:
	# 			store.append(current_grid)
	# 	if x >= 400 and (y >= 150 and y <= 300):
	# 		current_grid = 6
	# 		if current_grid != store[-1]:
	# 			store.append(current_grid)
	# 	if x <= 200 and y >= 300:
	# 		current_grid = 7
	# 		if current_grid != store[-1]:
	# 			store.append(current_grid)
	# 	if (x >= 200 and x <= 400) and y >= 300:
	# 		current_grid = 8
	# 		if current_grid != store[-1]:
	# 			store.append(current_grid)
	# 	if x >= 400 and y >= 300:
	# 		current_grid = 9
	# 		if current_grid != store[-1]:
	# 			store.append(current_grid)

	# def store_flags(self):
	# 	store = []

	# 	if event.type == GRID:
	# 		if len(store) <= 4:
	# 			list_grids(store)
	# 		else:
	# 			store.remove(store[0])
	# 			list_grids(store)
	# 	return store 