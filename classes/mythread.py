# -*- coding: UTF-8 -*-

import re
import threading
import blocks
import myservo

class ColorCodeThread(threading.Thread):
	def __init__(self, threadID, name, brain, fSM):#, serial):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.brain = brain
		self.fSM = fSM
		#self.serial = serial

	def run(self):
		while 1:
		#self.serial.write("0,90,90,90,90")
			center = self.get_center_stick()

			if center['x'] > 200 and center['x'] < 285: 
				print "rotate left"
				#myservo.servoPos['rotationPos'] -= 1
			elif center['x'] > 0 and center['x'] < 200: 
				print "base left"
				#myservo.servoPos['basePos'] -= 1
			elif center['x'] > 355 and center['x'] < 440:
				print "rotate right"
				#myservo.servoPos['rotationPos'] += 1
			elif center['x'] > 440 and center['x'] < 640:
				print "base right"
				#myservo.servoPos['basePos'] += 1
			else:
				#print "deadzone x"
				pass

			if center['y'] > 100 and center['y'] < 175:
				print "head up"
				#myservo.servoPos['headPos'] -= 1
			elif center['y'] > 0 and center['y'] < 100:
				print "arm up"
				#myservo.servoPos['armPos'] -= 1
			elif center['y'] > 225 and center['y'] < 300:
				print "head down"
				#myservo.servoPos['headPos'] += 1
			elif center['y'] > 300 and center['y'] < 400:
				print "arm down"
				#myservo.servoPos['armPos'] += 1
			else:
				#print "deadzone y"
				pass

			#self.serial.write("0, {0}, {1}, {2}, {3}".format(myservo.servoPos['basePos'], myservo.servoPos['armPos'], myservo.servoPos['rotationPos'], myservo.servoPos['headPos']))

	def get_center_stick(self):
		center = {'x': 0, 'y': 0}
		center['x'] = blocks.block.x + (blocks.block.width / 2)
		center['y'] = blocks.block.y + (blocks.block.height / 2)

		return center

	def kill(self):
		threading._Thread_stop()

class VoiceThread(threading.Thread):
	def __init__(self, threadID, name, brain, fSM):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.brain = brain
		self.fSM = fSM

	def run(self):
<<<<<<< HEAD
		while 1:

			self.brain.ledRingColor['red'] = 5
			self.brain.ledRingColor['green'] = 30
			self.brain.ledRingColor['blue'] = 5

			#self.brain.ledRing.set_color(self.brain.ledRingColor)

			input = self.brain.mic.active_listen()
			print input
			if re.search(r'\b(power down|powerdown)\b', input, re.IGNORECASE):
				self.fSM.to_transition("toShutdown")
				break
			elif re.search(r'\b(dankje|tot ziens)\b', input, re.IGNORECASE):
				self.fSM.to_transition("toScanning")
				break
			else:
				self.brain.ledRingColor['red'] = 30
				self.brain.ledRingColor['green'] = 5
				self.brain.ledRingColor['blue'] = 5

				#self.brain.ledRing.set_color(self.brain.ledRingColor)
				self.brain.query(input)

	def kill(self):
		threading._Thread_stop()
=======
		self.brain.ledRingColor['red'] = 5
		self.brain.ledRingColor['green'] = 30
		self.brain.ledRingColor['blue'] = 5

		self.brain.ledRing.set_color(self.brain.ledRingColor)

		input = self.brain.mic.active_listen()
		print input
		if re.search(r'\b(power down|powerdown)\b', input, re.IGNORECASE):
			self.fSM.to_transition("toShutdown")
		elif re.search(r'\b(dankje|tot ziens)\b', input, re.IGNORECASE):
			self.fSM.to_transition("toScanning")
		else:
			self.brain.ledRingColor['red'] = 30
			self.brain.ledRingColor['green'] = 5
			self.brain.ledRingColor['blue'] = 5

			self.brain.ledRing.set_color(self.brain.ledRingColor)
			self.brain.query(input)
>>>>>>> parent of 8db5af2... geen led
