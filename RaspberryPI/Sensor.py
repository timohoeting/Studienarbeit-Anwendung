#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting       				   #
# Mail: mail[at]timohoeting.de  			   #
################################################

import RPi.GPIO as GPIO
import time
from ConfigReader import *
import threading

class MotionDetection(threading.Thread):
	def __init__(self, c):
		threading.Thread.__init__(self)
		global center
		center = c

	def run(self):
		# Use BCM GPIO references
		# instead of physical pin numbers
		GPIO.setmode(GPIO.BCM)
		reader = ConfigReader()

		# Festlegen der beiden Detection-Pins
		MOTION_PIN1 = int(reader.getMotionPin1())
		MOTION_PIN2 = int(reader.getMotionPin2())

		# Diese als Input definieren
		GPIO.setup(MOTION_PIN1,GPIO.IN)
		GPIO.setup(MOTION_PIN2,GPIO.IN)

		# Status definieren um verschiedene Änderungen zu erkennen
		Current_State_1  = 0
		Previous_State_1 = 0
		Current_State_2  = 0
		Previous_State_2 = 0

		try:
			center.writeLog('Motion Detection Status: OK')
			# Loop zur Erkennung einer Bewegung
			# Sensort erkennt Bewegung -> Signal = High
			# Wartet 3 Sekunden und setzt Signal = Low
			# Die LEDs werden nach bestimmter Zeit wieder
			# ausgeschaltet. Dies passiert in der Led-Klasse
			while True :
				# Aktuellen Status der Sensoren einlesen
				Current_State_1 = GPIO.input(MOTION_PIN1)
				Current_State_2 = GPIO.input(MOTION_PIN1)

				if (Current_State_1 == 1 and Previous_State_1 == 0 and Current_State_2 == 0):
					# Sensor 1 hat ausgelöst
					Previous_State_1 = 1
					center.motionDetected(0)

				if (Current_State_2 == 1 and Previous_State_2 == 0 and Current_State_1 == 0):
					# Sensor 2 hat ausgelöst
					Previous_State_2 = 1
					center.motionDetected(1)

				if (Current_State_1 == 0 and Previous_State_1 == 1):
					# Sensor 1 war an und ist wieder aus
					Previous_State_1 = 0

				if (Current_State_2 == 0 and Previous_State_2 == 1):
					# Sensor 2 war an und ist wieder aus
					Previous_State_2 = 0

				time.sleep(0.01)
		except KeyboardInterrupt:
			print "Quit"
			GPIO.cleanup()
