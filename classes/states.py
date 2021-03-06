# -*- coding: UTF-8 -*-

import config
import re
import time
import serial
import sys
import random

serServo = serial.Serial('/dev/ttyACM0', 19200)
serLed = serial.Serial('/dev/ttyACM1', 19200)

class State(object):
	def __init__(self, fSM, brain):
		self.fSM = fSM
		self.persona = r"\b" + config.config['name'] + "\\b"
		self.brain = brain

	def enter(self):
		pass

	def execute(self):
		pass

	def exit(self):
		pass

class Startup(State):
	def __init__(self, fSM, brain):
		super(Startup, self).__init__(fSM, brain)

	def enter(self):
		print "Entering startup"

	def execute(self):
		print "Starting up"
		self.brain.speaker.say("Beep")
		#time.sleep(1)
		self.brain.speaker.say("Boep ")
		#time.sleep(0.5)
		self.brain.speaker.say("What do you want from me!?")
		self.fSM.to_transition("toScanning")

	def exit(self):
		print "Startup complete"
		serServo.write("4")
		self.brain.speaker.say("Bow to your robot overlord")

class Scanning(State):
	def __init__(self, fSM, brain):
		super(Scanning, self).__init__(fSM, brain)

	def enter(self):
		print "Start Scanning"
		serServo.write("1")

	def execute(self):
		print "Scanning"
		serLed.write("30,0,30")

		input = self.brain.mic.active_listen()
		serLed.write("55,38,0")
		print(input)

		if input is not None:
			if re.search(self.persona, input, re.IGNORECASE):
				self.fSM.to_transition("toMove")
			else:
				defanswer = ('What did you say?!', 'Whatever tickles your fancy.', "I wouldn't say such things if I were you.")
				self.brain.speaker.say(random.choice(defanswer))

	def exit(self):
		print "Exit Scanning"

class Move(State):
	def __init__(self, fSM, brain):
		super(Move, self).__init__(fSM, brain)

	def enter(self):
		print "Start Moving"
		self.brain.speaker.say("What do you want from me!?")
		serServo.write("2")

	def execute(self):
		print "Moving to sound origin"
		#self.fSM.to_transition("toTrack")
		#super(Move, self).get_color_code()

		ccDetected = serServo.readline()
		print ccDetected
		if re.search("detected", ccDetected, re.IGNORECASE):
			self.fSM.to_transition("toTrack")
		elif re.search("failed", ccDetected, re.IGNORECASE):
			self.fSM.to_transition("toScanning")

		serLed.write("5,5,30")

	def exit(self):
		print "Stop Moving"
		#self.brain.speaker.say("Ik heb je gevonden")

class Track(State):
	def __init__(self, fSM, brain):
		super(Track, self).__init__(fSM, brain)

	def enter(self):
		print "Start Tracking"
		self.brain.speaker.say("There you are! I found you!")
		serServo.write("3")

	def execute(self):
		print "Tracking"
		serLed.write("5,30,5")

		input = self.brain.mic.active_listen()
		serLed.write("30,5,5")
		print input

		if input is not None:
			if re.search(r'\b(power down|powerdown)\b', input, re.IGNORECASE):
				self.fSM.to_transition("toShutdown")
			elif re.search(r'\b(dankje|tot ziens|thank you|bye)\b', input, re.IGNORECASE):
				self.brain.speaker.say("you are welcome. Bye Bye")
				self.fSM.to_transition("toScanning")
			else:
				self.brain.query(input)

	def exit(self):
		print "Stop Tracking"

class Shutdown(State):
	def __init__(self, fSM, brain):
		super(Shutdown, self).__init__(fSM, brain)

	def enter(self):
		print "Entering shutdown"
		self.brain.speaker.say("Shutting down.")

		# set servo's to transport position
		serServo.write("5")
		serLed.write("0,0,0")

	def execute(self):
		print "Shutting down"

		input = self.brain.mic.active_listen()
		print input
		if re.search(r'\b(opstarten|start up)\b', input, re.IGNORECASE):
			self.fSM.to_transition("toStartup")

	def exit(self):
		print "Exit shutdown"

class DemoStartup(State):
	def __init__(self, fSM, brain):
		super(DemoStartup, self).__init__(fSM, brain)

	def enter(self):
		print "Entering Demo startup"

	def execute(self):
		print "Demo starting up"
		self.brain.speaker.say("Starting Demo function")
		self.fSM.to_transition("toDemo")

	def exit(self):
		print "Demo startup complete"
		serServo.write("4")
		self.brain.speaker.say("Running Demo function")

class Demo(State):
	def __init__(self, fSM, brain):
		super(Demo, self).__init__(fSM, brain)

	def enter(self):
		print "Entering demo"
		serLed.write("55, 38, 0")
		serServo.write("3")

	def execute(self):
		print "Demo running"

		input = self.brain.mic.active_listen()
		print input
		if re.search(r'\bexit demo\b', input, re.IGNORECASE):
			self.fSM.to_transition("toStartup")

	def exit(self):
		print "Exit Demo"
		serServo.write("5")
		serLed.write("0,0,0")
