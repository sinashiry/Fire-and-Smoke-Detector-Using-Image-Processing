# -*- coding: utf-8 -*-

#####################################################
#    Project:     Fire & Smoke Detection            #
#    Designer:    Hossein AalamShahi                #
#    Programmer:  Sina Shiri                        #
#    Date:        2019 Jul 25                       #
#    For:         Ista Sanat Co.                    #
#    File:        Sync System Time from SQL SERVER  #
#####################################################

from cryptography.fernet import Fernet
import pyodbc
import threading
import jdatetime
import datetime
import subprocess
import time

# Thread Duration for sync Time of RPi
set_time_thread = 10
set_time_thread_per = 3600
        
months = {"01":"Jan","02":"Feb","03":"Mar","04":"Apr","05":"May","06":"Jun",
          "07":"Jul","08":"Aug","09":"Sep","10":"Oct","11":"Nov","12":"Dec"}


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
	
	#Sync Database info.
	sqlServer = db_ip
	sqlPort = db_pt
	sqlUsername = db_us
	sqlPassword = db_ps
	sqlDatabase = db_nm

else:
	None




# Configure time location
jdatetime.set_locale('fa_IR')

# Pyodbc Config.
SQL_ATTR_CONNECTION_TIMEOUT = 113
login_timeout = 10
connection_timeout = 10

def set_datetime():
    try:
        output = pyodbc.connect('DRIVER=FreeTDS;SERVER='+sqlServer+';PORT='+sqlPort+';DATABASE='+
                                sqlDatabase+';UID='+sqlUsername+';PWD='+sqlPassword, timeout=login_timeout, 
                                attrs_before={SQL_ATTR_CONNECTION_TIMEOUT: connection_timeout})
        cur = output.cursor()
        cur.execute("SELECT SYSDATETIME()").description
        serverDatetime = cur.fetchall()[0][0]
        now = serverDatetime[8:10] + " " + months[serverDatetime[5:7]] + " "
        now = now + serverDatetime[0:4] + " " + serverDatetime[11:19]
        output = subprocess.Popen(["sudo","date","-s",now],stdout = subprocess.PIPE).communicate()[0]
        #print(now)
        #print(output)
        print("#########################")
        print("RPi Time same as SQL NTP Server")
        cur.close
        threading.Timer(set_time_thread_per, set_datetime).start()
    except:
        print("#########################")
        print ("RPi Cant Get SQL NTP Server")
        threading.Timer(set_time_thread, set_datetime).start()
        
set_datetime()
