# -*- coding: utf-8 -*-

#####################################################
#    Project:     Fire & Smoke Detection            #
#    Designer:    Hossein AalamShahi                #
#    Programmer:  Sina Shiri                        #
#    Date:        2019 Jul 25                       #
#    For:         Ista Sanat Co.                    #
#    File:        Check all section if need         #
#####################################################

# Needed Module(s)
import RPi.GPIO as GPIO
import time
import threading
import pyodbc
import subprocess
from cryptography.fernet import Fernet
import SIM800
import serial
import sqlite3
import os
import psutil

# Declare GPIO's Name
GPIOSIM800 = 26
GPIONET = 19
GPIOLOCALN  = 13
GPIOLOCALS = 6
#-------------
SIM800_RESET = 18
#-------------
AR_Button = 17
SD_Button = 27
#-------------
AlarmEN = 4
preAlarmEN = 22
#--------NN check
nnToggle = 21


# Setup GPIOs
GPIO.setmode(GPIO.BCM)

GPIO.setup(AlarmEN, GPIO.OUT)
GPIO.output(AlarmEN, False)

GPIO.setup(preAlarmEN, GPIO.OUT)
GPIO.output(preAlarmEN, False)

GPIO.setup(SIM800_RESET, GPIO.OUT)
GPIO.output(SIM800_RESET, True)

GPIO.setup(GPIOLOCALS, GPIO.OUT)
GPIO.setup(GPIOLOCALN, GPIO.OUT)
GPIO.setup(GPIONET, GPIO.OUT)
GPIO.setup(GPIOSIM800, GPIO.OUT)
GPIO.setup(nnToggle, GPIO.OUT)
GPIO.output(GPIOLOCALS, False)
GPIO.output(GPIOLOCALN, False)
GPIO.output(GPIONET, False)
GPIO.output(GPIOSIM800, False)
GPIO.output(nnToggle,False)

def releaseAlarm(channel):
    time.sleep(1)
    a = GPIO.input(AR_Button)
    if a == True:
        GPIO.output(AlarmEN, False)
        GPIO.output(preAlarmEN, False)
    
GPIO.setup(AR_Button,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(AR_Button, GPIO.RISING, callback=releaseAlarm, bouncetime=300)

def setDefault(channel):
    time.sleep(3)
    a = GPIO.input(SD_Button)
    if a == True:
        # copy default settings
        os.system("rm -r /home/pi/IS/settings/settings")
        os.system("cp /home/pi/IS/settings/default/settings /home/pi/IS/settings/")
        # reboot system
        os.system("(sleep 5; reboot) &")
    
GPIO.setup(SD_Button,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(SD_Button, GPIO.RISING, callback=setDefault, bouncetime=300)


# Timers
localnTimer = 20
localsTimer = 20
netTimer = 20
sim800Timer = 20
DBTimer = 180

# Pyodbc Config.
SQL_ATTR_CONNECTION_TIMEOUT = 113
login_timeout = 10
connection_timeout = 10

# Get User Settings
### Get Basic Info from Settings ###
# Read Decryption Key
file = open('/home/pi/IS/encryption/key.key', 'rb')
key = file.read()
f = Fernet(key)
file.close()
# Open Encrypted File
file_ = open('/home/pi/IS/settings/settings', 'rb')
data = file_.read()
file_.close()
# Settings in STR
settingsStr = f.decrypt(data).decode()

# Get needed Settings Value

# -SIM800 -Enable
gs_en = settingsStr[settingsStr.find("gs"):settingsStr.find("\n",settingsStr.find("gs"))]
gs_en = gs_en[gs_en.find("=")+1:]
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("gs"):settingsStr.find("\n",settingsStr.find("gs"))],"")

# -DB LOCAL -Enable
ws_en = settingsStr[settingsStr.find("ws"):settingsStr.find("\n",settingsStr.find("ws"))]
ws_en = ws_en[ws_en.find("=")+1:]
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("ws"):settingsStr.find("\n",settingsStr.find("ws"))],"")

# -DB LOCAL -Enable
db_en = settingsStr[settingsStr.find("db"):settingsStr.find("\n",settingsStr.find("db"))]
db_en = db_en[db_en.find("=")+1:]
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("db"):settingsStr.find("\n",settingsStr.find("db"))],"")

# -DB LOCAL -IP
db_ip = settingsStr[settingsStr.find("db"):settingsStr.find("\n",settingsStr.find("db"))]
db_ip = db_ip[db_ip.find("=")+1:]
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("db"):settingsStr.find("\n",settingsStr.find("db"))],"")

# -DB LOCAL -PORT
db_pt = settingsStr[settingsStr.find("db"):settingsStr.find("\n",settingsStr.find("db"))]
db_pt = db_pt[db_pt.find("=")+1:]
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("db"):settingsStr.find("\n",settingsStr.find("db"))],"")

# -DB LOCAL -USERNAME
db_us = settingsStr[settingsStr.find("db"):settingsStr.find("\n",settingsStr.find("db"))]
db_us = db_us[db_us.find("=")+1:]
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("db"):settingsStr.find("\n",settingsStr.find("db"))],"")

# -DB LOCAL -PASSWORD
db_ps = settingsStr[settingsStr.find("db"):settingsStr.find("\n",settingsStr.find("db"))]
db_ps = db_ps[db_ps.find("=")+1:]
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("db"):settingsStr.find("\n",settingsStr.find("db"))],"")

# -DB LOCAL -NAME
db_nm = settingsStr[settingsStr.find("db"):settingsStr.find("\n",settingsStr.find("db"))]
db_nm = db_nm[db_nm.find("=")+1:]
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("db"):settingsStr.find("\n",settingsStr.find("db"))],"")

imgPath = "/home/pi/IS/webserver/IMG_DB/"
dbPath = "/home/pi/IS/webserver/DB/events.db"


#Sync Database info.
sqlServer = db_ip
sqlPort = db_pt
sqlUsername = db_us
sqlPassword = db_ps
sqlDatabase = db_nm

###        FUNCTIONS        ###
# Check LOCAL NETWORK Connection
def checkNetworkConnection():
    # Show Thread Alive
    GPIO.output(GPIOLOCALN, False)
    time.sleep(0.5)
    # Get RPi IP in Network
    outputWLAN = subprocess.Popen(["ifconfig","wlan0"],stdout = subprocess.PIPE).communicate()[0].decode()
    outputETH = subprocess.Popen(["ifconfig","eth0"],stdout = subprocess.PIPE).communicate()[0].decode()
    # Set/Reset LOCALN LED
    if (outputWLAN.find("inet ") != -1 or outputETH.find("inet ") != -1):
        GPIO.output(GPIOLOCALN, True)
    else:
        GPIO.output(GPIOLOCALN, False)
    # Active Thread
    threading.Timer(localnTimer, checkNetworkConnection).start()

# Check LOCAL SERVER Connection
def checkServerConnection():
    # Show Thread Alive
    GPIO.output(GPIOLOCALS, False)
    time.sleep(0.5)
    # Get Table in SQL Server
    results_ = ""
    try:
        output = pyodbc.connect('DRIVER=FreeTDS;SERVER='+sqlServer+';PORT='+sqlPort+';DATABASE='+
                                sqlDatabase+';UID='+sqlUsername+';PWD='+sqlPassword, timeout=login_timeout, 
                                attrs_before={SQL_ATTR_CONNECTION_TIMEOUT: connection_timeout})
        cur = output.cursor()
        cur.execute("SELECT SYSDATETIME()").description
        results_ = cur.fetchall()[0][0]
        cur.close
    except:
        results_ = ""
    # Set/Reset LOCALS LED
    if (len(results_)>1):
        GPIO.output(GPIOLOCALS, True)
    else:
        GPIO.output(GPIOLOCALS, False)
    # Active Thread
    threading.Timer(localsTimer, checkServerConnection).start()

# Check INTERNET Connection
def checkInternetConnection():
    # Show Thread Alive
    GPIO.output(GPIONET, False)
    time.sleep(0.5)
    # Get RPi IP in PUBLIC
    publicIP = subprocess.Popen(["curl","ifconfig.me/ip"], stdout = subprocess.PIPE, stderr=subprocess.DEVNULL).communicate()[0].decode()
    # Set/Reset LOCALN LED
    if (len(publicIP)<16 and len(publicIP)>6):
        GPIO.output(GPIONET, True)
    else:
        GPIO.output(GPIONET, False)
    # Active Thread
    threading.Timer(netTimer, checkInternetConnection).start()

# Check INTERNET Connection
def checkSIM800Connection():
    # Show Thread Alive
    #GPIO.output(GPIOSIM800, False)
    #time.sleep(0.5)
    results_ = ""
    # Get SIM800 Status
    serialAddrss = "/dev/serial0"
    ser = serial.Serial(serialAddrss, baudrate=115200)
    for i in range(0,30):
        time.sleep(1)
        if(SIM800.isReady(ser) == True):
            for i in range(0,5):
                time.sleep(3)
                result = SIM800.signalPower(ser)
                if (result != "not known or not detectable" or result != "-115 dBm or less"):
                    results_ = "SIM800 STATUS = OK"
                    # Reset GSM Module
                    GPIO.output(SIM800_RESET, False)
                    time.sleep(1)
                    GPIO.output(SIM800_RESET, True)
                    break
                else:
                    None
            if (len(results_)>1):
                break
        else:
            None
    # Set/Reset SIM800 LED
    if (len(results_)>2):
        GPIO.output(GPIOSIM800, True)
    else:
        GPIO.output(GPIOSIM800, False)
    ser.close()
    # Active Thread
    #threading.Timer(sim800Timer, checkSIM800Connection).start()

def syncDB():
    # Get Data from SQLite
    addrss = sqlite3.connect(dbPath)
    cb = addrss.cursor()
    cb.execute('SELECT * FROM {tn} ORDER BY DTSR DESC'.\
                    format(tn="events"))
    allData = cb.fetchall()
    addrss.close()
    # Check Local DB Col.
    for i in range(0,len(allData)):
        if (allData[i][9]=="False"):
            try:
                output = pyodbc.connect('DRIVER=FreeTDS;SERVER='+db_ip+';PORT='+db_pt+';DATABASE='+db_nm+';UID='+db_us+';PWD='+db_ps, timeout=login_timeout, 
                                        attrs_before={SQL_ATTR_CONNECTION_TIMEOUT: connection_timeout})
                cur = output.cursor()
                # Storage Event in Local DB
                command = "INSERT INTO events (SERIAL_NUMBER, ZONE_NAME, ZONE_TYPE, EVENT, DATE, TIME, IMAGE, DTSR, EMERGENCY) "
                command = command + "VALUES ('"+allData[i][0]+"','"+allData[i][1]+"','"+allData[i][2]+"','"+allData[i][3]+"','"+allData[i][4]+"','"+allData[i][5]+"',"+"?, '"+allData[i][6]+"', '"+"-"+"')"
                #Get picture for Saving in DB
                data = open(imgPath+allData[i][7],'rb').read()
                cur.execute(command,(pyodbc.Binary(data),))
                cur.commit()
                cur.close()
                
                addrss = sqlite3.connect(dbPath)
                cb = addrss.cursor()
                cb.execute("UPDATE {tn} SET LOCAL_DB = '{vl}' WHERE DTSR = '{dt}'".\
                        format(tn="events", vl="True", dt=allData[i][6]))
                addrss.commit()
                addrss.close()
                
                print("DB UPDATED")
            
            except:
                print("Error in DB Connection")
    # Active Thread
    threading.Timer(DBTimer, syncDB).start()

#check System CPU Percentage    
def restartSystem():
	if(psutil.cpu_percent(interval=None) < 40.0):
		#reboot system
		os.system("reboot")
	threading.Timer(15, restartSystem).start()


# Get Check Each Section
checkNetworkConnection()
if (db_en == "True"):
    checkServerConnection()
if (ws_en == "True"):
    checkInternetConnection()
if (gs_en == "True"):
    checkSIM800Connection()
syncDB()
time.sleep(60)
restartSystem()
