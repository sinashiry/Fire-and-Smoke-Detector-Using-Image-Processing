#!/usr/bin/python
# -*- coding: utf-8 -*-

#####################################################
#    Project:     Fire & Smoke Detection            #
#    Designer:    Hossein AalamShahi                #
#    Programmer:  Sina Shiri                        #
#    Date:        2019 AUG 03                       #
#    For:         Ista Sanat Co.                    #
#    File:        ControlPanel (Delete DB files)    #
#####################################################


# Add Needed Modules
import os
from os.path import exists
import sqlite3

dbPath = "/home/pi/IS/webserver/DB/events.db"
imgdbPath = "/home/pi/IS/webserver/IMG_DB/*"

if (exists(dbPath)):
	os.remove(dbPath)
	os.system("rm -r " + imgdbPath)
	#os.system("cp /home/pi/IS/webserver/DB/D_events.db /home/pi/IS/webserver/DB/events.db")
	#os.system("sudo chmod 777 events.db")
