#!/usr/bin/python
# -*- coding: utf-8 -*-
################################################
# Author: Timo Höting                          #
# Mail: mail[at]timohoeting.de                 #
################################################
# Center of Application

from Server import *
from Sensor import *
from LED_Control import *
from Cam import *
import logging
import time
import datetime
import threading


class Core():
  def init(self):
    # Alle Initialisierungen vornehmen
    # Server = Webserver, der die Eingaben der App empfängt
    # Sensor = Klasse, welche die Bewegungssensoren auswertet
    # LED = Klasse zur LED Steuerung
    # Modus = Aktueller Modus in dem sich das System befindet
    # System wird in Modus 0 initialisiert (Bewegungsmelder an)
    global server
    server = StartLightServer(self)
    threads.append(server)
    global sensor
    sensor = MotionDetection(self)
    threads.append(sensor)
    global led
    led = NeoPixels()
    threads.append(led)
    global modus
    modus = 0
    self.startAll()

  def startAll(self):
    try:
        server.start()
    except IOError:
        print 'Error:', arg
    else:
        print 'Server gestartet'
    try:
        sensor.start()
    except IOError:
        print 'Error:', arg
    else:
        print 'Motion Detection gestartet'
    try:
        led.start()
    except IOError:
        print 'Error:', arg
    else:
        print 'LEDs initialisiert'

  def getModus(self):
      return modus

  def setModus(self, mod):
      # Modus
      # 0: Beleuchtung wird durch Bewegungsmelder ausgelöst
      # 1: Beleuchtung wird manuell vom Benutzer über App gesteuert
      # 2: Bewegungsmelder als Alarmanlage, beim Auslösen wird der
      #    Benutzer benachrichtigt und Bild der Kamera als Notification
      #    auf dem Smartphone angezeigt
      global modus
      modus = mod

  def motionDetected(self):
    # Wird bei Auslösen des Bewegungssensors aufgerufen
    if(modus == 0):
        led.motionLight()
    elif(modus == 2):
        self.alarm()

  def alarm(self):
      # Wird ausgelöst, wenn System im Modus 'Alarmanlage' ist
      # Meldung an Smartphone
      self.writeLog('Bewegung ausgelöst!')
      #cam = Cam()
      #pic = cam.getPicture()
      server.pushNotification('push')

  def clearPixel(self):
    # Alle Pixel ausschalten
    led.clear()

  def getLedStatus(self):
    # Ausgabe des Status
    print 'led status'

  def writeLog(self, content):
    # Message ins Logfile schreiben
    Ttime = time.time()
    formattedTime = datetime.datetime.fromtimestamp(Ttime).strftime('%Y-%m-%d %H:%M:%S')
    logging.basicConfig(filename='./log/all.log',level=logging.DEBUG)
    logging.warning(formattedTime + '| ' + content)

  def lightUpOneLED(self, ledNo, red, green, blue):
    # Eine einzelne LED mit den o.g. RGB-Werten dauerhaft anschalten
    if(modus == 1):
        led.onePixel(ledNo, red, green, blue)

  def lightUpLEDRange(self, rangeStart, rangeEnd, red, green, blue):
    # Einen Bereich von LEDs mit den o.g. RGB-Werten
    # dauerhaft einschalten
    if(modus == 1):
        led.rangePixel(rangeStart, rangeEnd, red, green, blue)

  def effectOneLED(self):
    # Effekte auf einer LED aktivieren
    print 'Effekt eine LED'

  def effectLEDRange(self):
    # Effekte auf einem LED-Bereich aktivieren
    if(modus == 1):
        print 'Effekte LED-Bereich'

  def runEffects(self, code):
    # Einprogrammierte Effekte starten
    led.runEffects(code)

  def printStatus(self):
    # Status ausgeben
    if(modus == 1):
        colours = led.getAllColours()


if __name__ == "__main__":
    threads = []
    core = Core()
    core.init()
