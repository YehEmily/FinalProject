"""Emily Yeh and Lydia Zuehsow"""

"""This program allows a person to wave a green "wand" to cast spells, Harry Potter-style!"""

"""For future reference, here's a link to our Google doc: https://docs.google.com/document/d/1daGjz8CWycfev0Fs96ru-Na5JNtqs2nVE1fHZ1ydhX0/edit?usp=sharing"""

# ****************** IMPORTED STUFF ****************** #

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

# ****************** CLASSES ****************** #

class WebCam(object):
	"""Runs the webcam and identifies green objects.
		return: center coordinates"""

	def __init__(self, bufsize = 100, counter = 0):
		self.camera = cv2.VideoCapture(0)
		self.ap = argparse.ArgumentParser()
		self.ap.add_argument("-v","--video",
			help="path to the(optional) video file")
		self.bufsize = bufsize
		self.ap.add_argument("-b", "--buffer", type=int, default = 100,
			help="max buffer size")
		self.pts = deque(maxlen=bufsize)
		self.rad = []
		self.counter = counter

	def getcenter(self, greenLower, greenUpper):
		self.args = vars(self.ap.parse_args())
		(self.grabbed, self.frame) = self.camera.read() # Grabs the current frame
		
		# Resizes the frame, blurs the frame, converts to HSV color space
		self.frame = imutils.resize(self.frame, width=600)
		blurred = cv2.GaussianBlur(self.frame,(11,11),0)
		hsv = cv2.cvtColor(self.frame,cv2.COLOR_BGR2HSV)

		# Constructs a mask for "green" objects, performs dilations and erosions to remove erroneous parts of the mask
		mask = cv2.inRange(hsv, greenLower, greenUpper)
		mask = cv2.erode(mask,None,iterations=1)
		mask = cv2.dilate(mask,None,iterations=1)

		# Finds contours in the mask, initializes the current (x,y) center
		self.cnts = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)[-2]

		# Only continue if at least one contour is found
		if len(self.cnts) > 0:
			# Find the largest contour in the mask, use it to compute the minimum enclosing circle and centroid for that contour
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
		# Draw a grid on the webcam stream for spell-casting
		cv2.line(webcam.frame, (0,0), (0,450), blueColor, 1)
		cv2.line(webcam.frame, (200,0), (200,450), blueColor, 1)
		cv2.line(webcam.frame, (400,0), (400,450), blueColor, 1)
		cv2.line(webcam.frame, (600,0), (600,450), blueColor, 1)
		cv2.line(webcam.frame, (0,0), (600,0), blueColor, 1)
		cv2.line(webcam.frame, (0,150), (600,150), blueColor, 1)
		cv2.line(webcam.frame, (0,300), (600,300), blueColor, 1)

		# Draw a dot to represent the wand's coordinates
		cv2.circle(webcam.frame, center, 5, blueColor, -1)

		# What happens next depends on whether the player is still alive or not
		if player.hp <= 0:
			cv2.rectangle(webcam.frame, (0,0), (600,450), (0,0,0), -1)
			img = cv2.imread('gameover.jpg')
			cv2.imshow('Game Over', img)
		else:
			cv2.rectangle(webcam.frame, (50,10), (550,30), greenColor, -1)
			cv2.rectangle(webcam.frame, (50,10), ((550 - player.hp),30), redColor, -1)


class Player(object):
	"""Represents you, the player!"""

	def __init__(self):
		self.hp = 500
		self.hit = False

	def DamageTaken(self,dmg):
		self.hp -= dmg


class Enemy(object):
	"""Represents your opponent."""

	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.hp = 100
		self.hit = False

	def Move(self, newx, newy):
		self.x = newx
		self.y = newy

	def DamageTaken(self,dmg):
		self.hp = self.hp - dmg

	def DamageDealt(self):
		self.damage = 10


class DesktopModel(object):
	"""Stores the fake desktop state."""

	def __init__(self):
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
		if (self.grid1flag and self.grid4flag and self.grid7flag) and (self.grid2flag == False and self.grid3flag == False and self.grid5flag == False and self.grid6flag == False and self.grid8flag == False and self.grid9flag == False) and (spell_frame <= 10):
			if spell_frame == 1:
				print 'You cast Flipendo!'
				enemy.DamageTaken(25)
			enemy.hit = True
			return
		
		elif (self.grid3flag and self.grid6flag and self.grid9flag) and (self.grid1flag == False and self.grid2flag == False and self.grid4flag == False and self.grid5flag == False and self.grid7flag == False and self.grid8flag == False) and (spell_frame <= 10):
			if spell_frame == 1:
				print 'You cast Wingardium leviosa!'
				enemy.DamageTaken(25)
			enemy.hit = True
			return

		elif (self.grid1flag and self.grid2flag and self.grid4flag and self.grid5flag) and (self.grid3flag == False and self.grid6flag == False and self.grid7flag == False and self.grid8flag == False and self.grid9flag == False) and (spell_frame <= 10):
			if spell_frame == 1:
				print 'You cast Incendio!'
				enemy.DamageTaken(50)
			enemy.hit = True
			return

		elif (self.grid2flag and self.grid4flag and self.grid5flag and self.grid6flag and self.grid8flag) and (self.grid1flag == False and self.grid3flag == False and self.grid7flag == False and self.grid9flag == False) and (spell_frame <= 10):
			if spell_frame == 1:
				print 'You cast Avada kedavra!'
				enemy.DamageTaken(100)
			enemy.hit = True
			return

		elif (self.grid3flag and self.grid4flag and self.grid5flag and self.grid6flag and self.grid7flag) and (self.grid1flag == False and self.grid2flag == False and self.grid8flag == False and self.grid9flag == False) and (spell_frame <= 10):
			if spell_frame == 1:
				print 'You cast Stupefy!'
				enemy.DamageTaken(100)
			enemy.hit = True
			return

		elif (self.grid3flag and self.grid5flag and self.grid6flag and self.grid7flag and self.grid8flag) and (self.grid1flag == False and self.grid2flag == False and self.grid4flag == False and self.grid9flag == False) and (spell_frame <= 10):
			if spell_frame == 1:
				print 'You cast Expelliarmus!'
				enemy.DamageTaken(100)
			enemy.hit = True
			return

		else:
			enemy.hit = False
			if player.hp > 0:
				dialogue = ["Voldemort takes a stab at you!", "Voldemort casts a spell-- it narrowly misses you!", "Voldemort realizes he doesn't have a nose and waves his wand in frustration!", "Voldemort screams something unintelligible and hits you with a weak spell!", "Voldemort unleashes a stream of curses! They're not very effective.", "Voldemort pauses for a moment to pick his nose, only to realize he doesn't have one.", "Voldemort calls forth an army of dementors, but they swarm around him excitedly like a bunch of puppies.", "Voldemort yells a hurtful insult at you!", "Voldemort bends down to pick up a tiny pebble and flings it at you! It hits you squarely in the stomach.", "Voldemort throws Nagini at you! Nagini is displeased.", "You tell Voldemort you just want to be friends. He gives you a scalding glare."]
			
				if random.randint(0,10) == 5:
					player.hit = True
					player.DamageTaken(10)
					dialogue_choose = dialogue[random.randint(0,9)]
					print dialogue_choose

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
	"""Visualizes a fake desktop in a pygame window."""

	def __init__(self,model,screen,background, winscreen, sprite, explosion):
		"""Initialise the view with a specific model."""
		self.model = model
		self.screen = screen.fill(whiteColor)

		# Load background png and post to screen
		background = pygame.image.load(background).convert()
		background = pygame.transform.scale(background, (screenwidth,screenheight))
		screen.blit(background,(0,0))

		# Lead the win screen
		self.winscreen = pygame.image.load(winscreen).convert()
		self.winscreen = pygame.transform.scale(self.winscreen, (screenwidth,screenheight))

		# Load enemy sprite png
		self.sprite = pygame.image.load(sprite).convert_alpha()

		# Load spell damage animation png
		self.explosion = pygame.image.load(explosion).convert_alpha()
		self.explosion = pygame.transform.scale(self.explosion, (250,250))

		# Draw the enemy's HP bar
		screen.fill((0,255,0),Rect(10,10,100,20))

		# Update game display
		pygame.display.update()

	def update(self):
		"""Draw the game state to the screen"""
		# Enemy spell damage animation
		if enemy.hit and (spell_frame <= 10):
			screen.blit(self.explosion,(enemy.x + 200,enemy.y + 150))
		else:
			screen.blit(self.sprite,(enemy.x,enemy.y))

		# Update the enemy's HP bar
		if enemy.hit and (spell_frame == 1) and enemy.hp > 0:
			screen.fill((255,0,0),Rect(10,10,(125 - enemy.hp),20))
		else:
			pass

		pygame.display.update()

	def wongame(self):
		screen.blit(self.winscreen,(0,0))
		pygame.display.update()


class Controller(object):
	"""Your controller is your green wand. Its position determines if you cast a spell or what spell you cast."""
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
					# print 'Grid 3'
					model.grid3flag = True
				if (x >= 200 and x <= 400) and y <=150:
					# print 'Grid 2'
					model.grid2flag = True
				if x >= 400 and y <= 150:
					# print 'Grid 1'
					model.grid1flag = True
				if x <= 200 and (y >= 150 and y <=300):
					# print 'Grid 6'
					model.grid6flag = True
				if (x >= 200 and x <= 400) and (y >= 150 and y <=300):
					# print 'Grid 5'
					model.grid5flag = True
				if x >= 400 and (y >= 150 and y <= 300):
					# print 'Grid 4'
					model.grid4flag = True
				if x <= 200 and y >= 300:
					# print 'Grid 9'
					model.grid9flag = True
				if (x >= 200 and x <= 400) and y >= 300:
					# print 'Grid 8'
					model.grid8flag = True
				if x >= 400 and y >= 300:
					# print 'Grid 7'
					model.grid7flag = True

		pygame.event.clear()

	def close(self):
		pygame.display.quit()
		pygame.quit()

if __name__ == '__main__':

# ****************** INITIALIZING STUFF ****************** #

	# Initialize pygame
	pygame.init()

	# Define some colors
	redColor = pygame.Color(0,0,255)
	greenColor = pygame.Color(0,255,0)
	blueColor = pygame.Color(255,0,0)
	whiteColor = pygame.Color(255,255,255)

	# Set pygame fake desktop size
	screenwidth = 600
	screenheight = 450

	size = (screenwidth, screenheight)
	screen = pygame.display.set_mode(size)

	model = DesktopModel()
	view = PygameView(model, screen, 'forbiddenforest.jpeg', 'win.png', 'volde.png', 'flame.png')
	master = Controller(model)

	# cursor = (blueColor,50,50,False)

# ****************** WEBCAM STUFF ****************** #

	#initialize stuff

	running = True
	frame = 0
	eventcount = 0
	webcam = WebCam()
	player = Player()

	greenLower = (29,86,6)
	greenUpper = (64,255,255)

	enemy = Enemy(25, 100)

	center = 0

	GRID = pygame.USEREVENT+2
	grid_event = pygame.event.Event(GRID)

	# Makes sure only the events we want are on the event queue
	allowed_events = [QUIT,GRID]
	pygame.event.set_allowed(allowed_events)

	buf = 10
	# "buf" is the buffer- the number of frames we go backwards 
	# to compare for movement- so if buf is 10, we compare 
	# the location of the "green" in the current frame 
	# to its location 10 frames earlier. 
	

# ****************** RUNTIME LOOP ****************** #
	# This is the main loop of the program. 
	spell_frame = 0

	while running:
		if enemy.hp <= 0:
			view.wongame()
		else:
			view.update()
			model.spell_check()

		# Check for spells
			if enemy.hit: #if a player's offensive spell is detected, add one to spell frame count
				spell_frame += 1
				if spell_frame > 3: #if a spell has finished firing, reset spell frame counter and clear all grid flags.
					model.spell_clear()
					spell_frame = 0
				else:
					pass
			else:
				pass

		# Find the center of any green objects' contours
		gotcenter = webcam.getcenter(greenLower, greenUpper)
		if gotcenter == None:
			webcam.update_webcam((300, 225))
		else:
			center = gotcenter[0]
			radius = gotcenter[1]
			webcam.update_webcam(center)
			if radius > 20:
				# If the radius is above a certain size we count it
				webcam.pts.append(center)
				webcam.rad.append(radius)
				webcam.counter = webcam.counter + 1
				(x,y) = center
				if (x >= 0 and x <= 600) and (y >= 0 and y <= 450):
					pygame.event.post(grid_event)

			master.process_events()

		# Update the frames of the webcam video
		webcam.frame = cv2.flip(webcam.frame, 1)
		cv2.imshow("Frame",webcam.frame)
		key = cv2.waitKey(1) & 0xFF
		frame = frame + 1
		time.sleep(.001)
		if key == ord("q"):
			running = False
			if running == False:
				# Release the camera, close open windows
				webcam.camera.release()
				cv2.destroyAllWindows()
				master.close()
		if key == ord("c"):
			model.spell_clear()
			
# ****************** CODE FOR STUFF WE MIGHT NOT NEED ****************** #

# class Mouse(object):
# 	"""Represents your spell trail"""
# 	def __init__(self,color,x=50,y=50,selected=False):
# 		self.x = x
# 		self.y = y
# 		self.color = color
# 		self.selected = selected

# 	def set_pos(self, x, y):
# 		self.x = x
# 		self.y = y
# 		# self.color = redColor

# 	def Move(self):
# 		gotcenter = webcam.getcenter(greenLower, greenUpper)
# 		if gotcenter == None:
# 			pass
# 		else:
# 			center = gotcenter[0]
# 			self.x = center[0]
# 			self.y = center[1]
# 		self.set_pos(self.x, self.y)



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