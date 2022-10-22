# -*- coding: utf-8 -*-

#####################################################
#    Project:     Fire & Smoke Detection            #
#    Designer:    Hossein AalamShahi                #
#    Programmer:  Sina Shiri                        #
#    Date:        2019 Jul 13                       #
#    For:         Ista Sanat Co.                    #
#    File:        SIM800 Module Using File          #
#####################################################

# Module(s)
import SIM800 as sim
import serial
import time, subprocess

# Data from Settings
serialAddrss = "/dev/serial0"

# Configuration of Serial Port
#ser = ""
#def startSerialPort():
ser = serial.Serial(serialAddrss, baudrate=115200)


def sendSMS(receiver, message):
	# Open Serial Port
	#->startSerialPort()
	# Reset GSM Module
	#sim.resetModem()
	for i in range(0,30):
		time.sleep(1)
		if(sim.isReady(ser) == True):
			for i in range(0,5):
				time.sleep(3)
				result = sim.signalPower(ser)
				if (result != "not known or not detectable" or result != "-115 dBm or less"):
					try:
						sim.sendSMS(ser, receiver, message)
						# Reset GSM Module
						sim.resetModem()
						return True
					except:
						# Reset GSM Module
						sim.resetModem()
						return False
				else:
					None
		else:
			None
	return False


def sendIMG(apn, filename, path, ftpPath, ftpAddrss, ftpPort, ftpUser, ftpPass):
	# Open Serial Port
	#->startSerialPort()
	# Reset GSM Module
	#sim.resetModem()
	for i in range(0,10):
		time.sleep(1)
		if(sim.isReady(ser) == True):
			for i in range(0,2):
				time.sleep(3)
				result = sim.signalPower(ser)
				if (result != "not known or not detectable" or result != "-115 dBm or less"):
					try:
						sim.connectGPRS(ser,apn)
						time.sleep(2)
						sim.sendFTP(ser,filename, path, ftpPath, ftpAddrss, ftpPort, ftpUser, ftpPass)
						# Reset GSM Module
						sim.resetModem()
						return True
					except:
						# Reset GSM Module
						sim.resetModem()
						return False
				else:
					None
		else:
			None
	return False

def sendEVENT(URL, host, port, apn):
	# Open Serial Port
	#->startSerialPort()
	# Reset GSM Module
	#sim.resetModem()
	for i in range(0,30):
		time.sleep(1)
		if(sim.isReady(ser) == True):
			for i in range(0,5):
				time.sleep(3)
				result = sim.signalPower(ser)
				if (result != "not known or not detectable" or result != "-115 dBm or less"):
					result = False
					try:
						sim.connectGPRS(ser,apn)
						time.sleep(2)
						sim.connectTCP(ser, host, port)
						time.sleep(2)
						contents = sim.sendHTTPRequest(ser, URL, host)
						if (contents.find("New record created successfully")):
							result = True
						else:
							result = False
						# Reset GSM Module
						sim.resetModem()
					except:
						# Reset GSM Module
						sim.resetModem()
					return result
				else:
					None
		else:
			None
	return False
