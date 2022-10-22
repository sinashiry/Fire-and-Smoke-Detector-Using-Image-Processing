# -*- coding: utf-8 -*-

#####################################################
#    Project:     Fire & Smoke Detection            #
#    Designer:    Hossein AalamShahi                #
#    Programmer:  Sina Shiri                        #
#    Date:        2019 Jul 21                       #
#    For:         Ista Sanat Co.                    #
#    File:        Alarm Main Controller             #
#####################################################

'''
Using Method:
		python3 alarm.py -event:[prealarm][fire][smoke] -filename:[ex:20190830_1304.jpg]
'''

# Modules
from cryptography.fernet import Fernet
import sys, subprocess
import sim800 as gsm
import jdatetime as jdt
import time
from PIL import Image
import pyodbc
from ftplib import FTP 
import os
from os.path import exists
import fileinput
import urllib.request
import socket
import sqlite3
import RPi.GPIO as GPIO

# Global Variable(s)
sm_msg  = "Emergency Alarm!\n"
sm_msg += "Event: #event\n"
sm_msg += "Zone: #zone\n"
sm_msg += "Date: #date\n"
sm_msg += "Time: #time\n"
imgPath = "/home/pi/IS/webserver/IMG_DB/"
localSQLitePath = "/home/pi/IS/webserver/DB/events.db"
resultURL = "/fire/results.php"
imgQuality = 45
REMOTE_SERVER = "www.google.com"

LOCAL_DB_SUCCESS = None
WEBSERVER_DB_SUCCESS = None
METHOD = None
SMS_SECCESS = None


# Some Needed Functions
# - Get RPi Serial Number
def getSerial():
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo','r')
        for line in f:
            if line[0:6]=='Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"
    return cpuserial

# - Get Internet 
def checkInternet(hostname):
    try:
        # see if we can resolve the host name
        host = socket.gethostbyname(hostname)
        # connect to the host
        s = socket.create_connection((host, 80))
        s.close()
        return True
    except:
        pass
    return False

def checkDBFile():
	if not(exists(localSQLitePath)):
		conn_db = sqlite3.connect(localSQLitePath)
		conn_db.execute('''CREATE TABLE events(
				SERIAL_NUMBER	TEXT	NOT NULL,
				ZONE_NAME   TEXT	NOT NULL,
				ZONE_TYPE   TEXT    NOT NULL,
                EVENT	TEXT	NOT NULL,
				DATE    TEXT    NOT NULL,
                TIME    TEXT    NOT NULL,
                DTSR    datetime    DEFAULT (datetime('now','localtime')),
                IMAGE   TEXT    NOT NULL,
                EMERGENCY   TEXT    NOT NULL,
                LOCAL_DB   TEXT    NOT NULL,
                WEB_SERVER   TEXT    NOT NULL,
                METHOD   TEXT    NOT NULL,
                SMS   TEXT    NOT NULL);''')
		conn_db.close()
	else:
		None


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

# -Zone -Name
zn_nm = settingsStr[settingsStr.find("zn"):settingsStr.find("\n",settingsStr.find("zn"))]
zn_nm = zn_nm[zn_nm.find("=")+1:]
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("zn"):settingsStr.find("\n",settingsStr.find("zn"))],"")

# -Zone -Mode
zn_md = settingsStr[settingsStr.find("zn"):settingsStr.find("\n",settingsStr.find("zn"))]
zn_md = zn_md[zn_md.find("=")+1:]
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("zn"):settingsStr.find("\n",settingsStr.find("zn"))],"")

# -SMS -Enable
sm_en = settingsStr[settingsStr.find("sm"):settingsStr.find("\n",settingsStr.find("sm"))]
sm_en = sm_en[sm_en.find("=")+1:]
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("sm"):settingsStr.find("\n",settingsStr.find("sm"))],"")

sm_pn_list = ""
if (sm_en == "True"):
	# -SMS -Number(s)
	sm_pn = settingsStr[settingsStr.find("sm"):settingsStr.find("\n",settingsStr.find("sm"))]
	sm_pn = sm_pn[sm_pn.find("=")+1:]
	settingsStr = settingsStr.replace(settingsStr[settingsStr.find("sm"):settingsStr.find("\n",settingsStr.find("sm"))],"")
	sm_pn_list = list()
	sm_pn_list = sm_pn.split(",")
else:
	None

# -GSM -Enable
gs_en = settingsStr[settingsStr.find("gs"):settingsStr.find("\n",settingsStr.find("gs"))]
gs_en = gs_en[gs_en.find("=")+1:]
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("gs"):settingsStr.find("\n",settingsStr.find("gs"))],"")

gs_ap = ""
if(gs_en == "True"):
    # -GSM -APN
    gs_ap = settingsStr[settingsStr.find("gs"):settingsStr.find("\n",settingsStr.find("gs"))]
    gs_ap = gs_ap[gs_ap.find("=")+1:]
    settingsStr = settingsStr.replace(settingsStr[settingsStr.find("gs"):settingsStr.find("\n",settingsStr.find("gs"))],"")

# -DB LOCAL -Enable
db_en = settingsStr[settingsStr.find("db"):settingsStr.find("\n",settingsStr.find("db"))]
db_en = db_en[db_en.find("=")+1:]
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("db"):settingsStr.find("\n",settingsStr.find("db"))],"")

db_ip = ""; db_pt = ""; db_us = ""; db_ps = ""; db_nm = ""
if (db_en == "True"):
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
else:
	None

# -Web SERVER -Enable
ws_en = settingsStr[settingsStr.find("ws"):settingsStr.find("\n",settingsStr.find("ws"))]
ws_en = ws_en[ws_en.find("=")+1:]
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("ws"):settingsStr.find("\n",settingsStr.find("ws"))],"")

ws_ad = ""; ws_ul = ""; fp_ad = ""; fp_pt = ""; fp_us = ""; fp_ps=""
if (ws_en == "True"):
	# -Web SERVER -Address
	ws_ad = settingsStr[settingsStr.find("ws"):settingsStr.find("\n",settingsStr.find("ws"))]
	ws_ad = ws_ad[ws_ad.find("=")+1:]
	settingsStr = settingsStr.replace(settingsStr[settingsStr.find("ws"):settingsStr.find("\n",settingsStr.find("ws"))],"")
	
	# -Web SERVER -URL
	ws_ul = settingsStr[settingsStr.find("ws"):settingsStr.find("\n",settingsStr.find("ws"))]
	ws_ul = ws_ul[ws_ul.find("=")+1:]
	settingsStr = settingsStr.replace(settingsStr[settingsStr.find("ws"):settingsStr.find("\n",settingsStr.find("ws"))],"")
	
	# -FTP SERVER -Address
	fp_ad = settingsStr[settingsStr.find("fp"):settingsStr.find("\n",settingsStr.find("fp"))]
	fp_ad = fp_ad[fp_ad.find("=")+1:]
	settingsStr = settingsStr.replace(settingsStr[settingsStr.find("fp"):settingsStr.find("\n",settingsStr.find("fp"))],"")
	
	# -FTP SERVER -Port
	fp_pt = settingsStr[settingsStr.find("fp"):settingsStr.find("\n",settingsStr.find("fp"))]
	fp_pt = fp_pt[fp_pt.find("=")+1:]
	settingsStr = settingsStr.replace(settingsStr[settingsStr.find("fp"):settingsStr.find("\n",settingsStr.find("fp"))],"")
	
	# -FTP SERVER -Username
	fp_us = settingsStr[settingsStr.find("fp"):settingsStr.find("\n",settingsStr.find("fp"))]
	fp_us = fp_us[fp_us.find("=")+1:]
	settingsStr = settingsStr.replace(settingsStr[settingsStr.find("fp"):settingsStr.find("\n",settingsStr.find("fp"))],"")
	
	# -FTP SERVER -Password
	fp_ps = settingsStr[settingsStr.find("fp"):settingsStr.find("\n",settingsStr.find("fp"))]
	fp_ps = fp_ps[fp_ps.find("=")+1:]
	settingsStr = settingsStr.replace(settingsStr[settingsStr.find("fp"):settingsStr.find("\n",settingsStr.find("fp"))],"")
else:
	None

# -Pre-Alarm -Enable
pa_en = settingsStr[settingsStr.find("pa"):settingsStr.find("\n",settingsStr.find("pa"))]
pa_en = pa_en[pa_en.find("=")+1:]
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("pa"):settingsStr.find("\n",settingsStr.find("pa"))],"")

# -Alarm -Enable
al_en = settingsStr[settingsStr.find("al"):settingsStr.find("\n",settingsStr.find("al"))]
al_en = al_en[al_en.find("=")+1:]
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("al"):settingsStr.find("\n",settingsStr.find("al"))],"")


# Pyodbc Config.
SQL_ATTR_CONNECTION_TIMEOUT = 113
login_timeout = 10
connection_timeout = 10

###     Get Arguments      ###
event = sys.argv[1][7:]
fileName = sys.argv[2][10:]

### Get Time-Date from RTC ### 
date_ = str(jdt.datetime.now())[:10]
time_ = str(jdt.datetime.now())[11:-7]

### Get RPi Serial Number  ### 
serialNumber = getSerial()

###   Reduce Image Size   ###
cache = Image.open(imgPath+fileName)
#cache = cache.resize(480,640)
cache.save(imgPath+fileName,quality=imgQuality)

###  Create GET HTTP URL   ### 
url  = "http://" + ws_ad + ws_ul + "?"
url += "serNum=" + serialNumber
url += "&zn_nm=" + zn_nm
url += "&zn_tp=" + zn_md
url += "&event=" + event
url += "&date=" + date_
url += "&time=" + time_
url += "&img=" + fileName
url += "&emrg=" + "-"

emrg = "-"

print("#########################")

### Active EMRG Pre-Alarm Output ###
preAlarmEN = 22
if (pa_en == "True" and event == "prealarm"):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(preAlarmEN, GPIO.OUT)
    GPIO.output(preAlarmEN, True)
    time.sleep(1)
    print("Pre-Alarm Activated")

### Active EMRG Alarm Output ###
AlarmEN = 4
if (al_en == "True" and event == "fire"):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(AlarmEN, GPIO.OUT)
    GPIO.output(AlarmEN, True)
    time.sleep(1)
    print("Alarm Activated")


### Get Local DB (SQL Server) ###
if (db_en == "True"):
    print("DB Section Started")
    # Get check Local Server Ping
    # Get Servers ping
    #output = subprocess.Popen(["ping","-w","1","-c","1",db_ip],stdout = subprocess.PIPE).communicate()[0]
    #output = output.decode("utf-8")
    #for i in range(0,4):
    #    if (' 0% packet loss' in output): ,
    #			timeout=login_timeout, attrs_before={SQL_ATTR_CONNECTION_TIMEOUT: connection_timeout}
    try:
        output = pyodbc.connect('DRIVER=FreeTDS;SERVER='+db_ip+';PORT='+db_pt+';DATABASE='+db_nm+';UID='+db_us+';PWD='+db_ps, 
                                    attrs_before={SQL_ATTR_CONNECTION_TIMEOUT: connection_timeout})
        cur = output.cursor()
        # Storage Event in Local DB
        command = "INSERT INTO events (SERIAL_NUMBER, ZONE_NAME, ZONE_TYPE, EVENT, DATE, TIME, IMAGE, EMERGENCY) "
        command = command + "VALUES ('"+serialNumber+"','"+zn_nm+"','"+zn_md+"','"+event+"','"+date_+"','"+time_+"',"+"?, '"+emrg+"')"
        #Get picture for Saving in DB
        data = open(imgPath+fileName,'rb').read()
        cur.execute(command,(pyodbc.Binary(data),))
        cur.commit()
        cur.close
        LOCAL_DB_SUCCESS = True
        print("DB Section Ended")
        #break
    except:
        LOCAL_DB_SUCCESS = False
        #break
    #    else:
    #        LOCAL_DB_SUCCESS = False
else:
    LOCAL_DB_SUCCESS = None



###Get Web Server Database (Wi/Eth)###
# 1st Step: Send Image to FTP Server
if (ws_en == "True"):
    print("WS Section Started")
    if (checkInternet(REMOTE_SERVER)):
        try:
            # Intialize FPT Connection
            ftp = FTP()
            ftp.set_debuglevel(2)
            ftp.connect(fp_ad, int(fp_pt)) 
            ftp.login(fp_us,fp_ps)
            # Change Path to IMG_DB
            try:
                ftp.cwd("IMG_DB")
            except:
                ftp.mkd("IMG_DB")
                ftp.cwd("IMG_DB")
            # Change Path to Serial_Number
            try:
                ftp.cwd(getSerial())
            except:
                ftp.mkd(getSerial())
                ftp.cwd(getSerial())
            # Save Pic in Server
            fp = open(imgPath+fileName, 'rb')
            ftp.storbinary('STOR %s' % os.path.basename(fileName), fp, 1024)
            fp.close()
        except:
            None
        try:
            # 2nd Step: HTTP Request for Send Event
            url += "&meth=" + "Adapter"
            contents = urllib.request.urlopen(url).read().decode()
            if (contents.find("New record created successfully")):
                WEBSERVER_DB_SUCCESS = True
                METHOD = "Adapter"
                print("WS Section Ended")
            else:
                WEBSERVER_DB_SUCCESS = False
        except:
            WEBSERVER_DB_SUCCESS = False
    elif (gs_en == "True"):
        ###Get Web Server Database (GSM)###
        # 1st Step: Send Image to FTP Server (GSM)
        try:
            # Send Pic via GSM (FPT)
            gsm.sendIMG(gs_ap, fileName, imgPath, "/IMG_DB"+"/"+getSerial()+"/", fp_ad, fp_pt, fp_us, fp_ps)
        except:
            None
        try:
            # 2nd Step: HTTP Request for Send Event (GSM)
            url += "&meth=" + "SIM800"
            url = url.replace("http://", "").replace(ws_ad, "")
            result = gsm.sendEVENT(url, ws_ad, 80, gs_ap)
            if (result):
                WEBSERVER_DB_SUCCESS = True
                METHOD = "SIM800"
                print("WS Section Ended")
            else:
                WEBSERVER_DB_SUCCESS = False
        except:
            WEBSERVER_DB_SUCCESS = False
    else:
        None
else:
    WEBSERVER_DB_SUCCESS = None
    METHOD = None


###        SEND SMS        ###
if (sm_en == "True" and event != "prealarm"):
    print("SMS Section Started")
    # Edit SMS Message
    sm_msg = sm_msg.replace("#event",event,1)
    sm_msg = sm_msg.replace("#zone",zn_nm,1)
    sm_msg = sm_msg.replace("#date",date_,1)
    sm_msg = sm_msg.replace("#time",time_,1)
    
    if (ws_en == "True" and WEBSERVER_DB_SUCCESS == True):
        sm_msg += "http://" + ws_ad + resultURL
    # Start Sending Process for All Phone Numbers
    deliver = list() 
    for i in range(0,len(sm_pn_list)):
        if (sm_pn_list[i].find("*") != -1):
            deliver.append(gsm.sendSMS(sm_pn_list[i].replace("*", ""),sm_msg))
        else:
            deliver.append("None")
    SMS_SECCESS = ""
    print("SMS Section Ended")
    for i in range(0,len(sm_pn_list)):
        if deliver[i] == True:
            SMS_SECCESS += "[True] "
        elif deliver[i] == False:
            SMS_SECCESS += "[False] "
        else:
            SMS_SECCESS += "[None] "
else:
    SMS_SECCESS = None


###Get Local DB (SQLite on RP)###
# Check DB File
checkDBFile()
# Record new event and info. in database file
conn_db = sqlite3.connect(localSQLitePath)
conn_db.execute("INSERT INTO events (SERIAL_NUMBER, ZONE_NAME, ZONE_TYPE," +
                "EVENT, DATE, TIME, IMAGE, EMERGENCY, LOCAL_DB, WEB_SERVER, METHOD, SMS) " +
                " VALUES ('"+serialNumber+"','"+zn_nm+"','"+zn_md+"','"+event+"','"+date_+"','"+
                time_+"','" + fileName + "','"+emrg+"','"+str(LOCAL_DB_SUCCESS)+"','"+
                str(WEBSERVER_DB_SUCCESS)+"','"+str(METHOD)+"','"+str(SMS_SECCESS)+"')")
conn_db.commit()
conn_db.close()
