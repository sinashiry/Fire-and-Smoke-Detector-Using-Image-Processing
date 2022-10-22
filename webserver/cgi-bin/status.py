#!/usr/bin/python
# -*- coding: utf-8 -*-

#####################################################
#    Project:     Fire & Smoke Detection            #
#    Designer:    Hossein AalamShahi                #
#    Programmer:  Sina Shiri                        #
#    Date:        2019 Jul 26                       #
#    For:         Ista Sanat Co.                    #
#    File:        ControlPanel (Status Page)        #
#####################################################

# Add Needed Modules
from cryptography.fernet import Fernet
import os
import subprocess
import time
import cgi
import pyodbc
import psutil

output = subprocess.Popen(["hostname","-I"],stdout = subprocess.PIPE).communicate()[0]
if (len(output)>15):
    ipaddr = output[:output.find(" ")]
else:
    ipaddr = output[:-2]

#Get Prev. Page Values
form = cgi.FieldStorage()
# Login INFO
sius = form.getvalue('si_us')
sips = form.getvalue('si_ps')

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

# -Login -Username
si_us = settingsStr[settingsStr.find("si"):settingsStr.find("\n",settingsStr.find("si"))]
si_us = si_us[si_us.find("=")+1:]
si_us = si_us.replace('"','&quot;')
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("si"):settingsStr.find("\n",settingsStr.find("si"))],"")

# -Login -Password
si_ps = settingsStr[settingsStr.find("si"):settingsStr.find("\n",settingsStr.find("si"))]
si_ps = si_ps[si_ps.find("=")+1:]
si_ps = si_ps.replace('"','&quot;')
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("si"):settingsStr.find("\n",settingsStr.find("si"))],"")


# -Company -Name
co_nm = settingsStr[settingsStr.find("co"):settingsStr.find("\n",settingsStr.find("co"))]
co_nm = co_nm[co_nm.find("=")+1:]
co_nm = co_nm.replace('"','&quot;')
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("co"):settingsStr.find("\n",settingsStr.find("co"))],"")


# -Firmware -Version
fr_vr = settingsStr[settingsStr.find("fr"):settingsStr.find("\n",settingsStr.find("fr"))]
fr_vr = fr_vr[fr_vr.find("=")+1:]
fr_vr = fr_vr.replace('"','&quot;')
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("fr"):settingsStr.find("\n",settingsStr.find("fr"))],"")


# -DB LOCAL -Enable
db_en = settingsStr[settingsStr.find("db"):settingsStr.find("\n",settingsStr.find("db"))]
db_en = db_en[db_en.find("=")+1:]
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("db"):settingsStr.find("\n",settingsStr.find("db"))],"")

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
    db_us = db_us.replace('"','&quot;')
    settingsStr = settingsStr.replace(settingsStr[settingsStr.find("db"):settingsStr.find("\n",settingsStr.find("db"))],"")

    # -DB LOCAL -PASSWORD
    db_ps = settingsStr[settingsStr.find("db"):settingsStr.find("\n",settingsStr.find("db"))]
    db_ps = db_ps[db_ps.find("=")+1:]
    db_ps = db_ps.replace('"','&quot;')
    settingsStr = settingsStr.replace(settingsStr[settingsStr.find("db"):settingsStr.find("\n",settingsStr.find("db"))],"")

    # -DB LOCAL -NAME
    db_nm = settingsStr[settingsStr.find("db"):settingsStr.find("\n",settingsStr.find("db"))]
    db_nm = db_nm[db_nm.find("=")+1:]
    db_nm = db_nm.replace('"','&quot;')
    settingsStr = settingsStr.replace(settingsStr[settingsStr.find("db"):settingsStr.find("\n",settingsStr.find("db"))],"")

    #Sync Database info.
    sqlServer = db_ip
    sqlPort = db_pt
    sqlUsername = db_us
    sqlPassword = db_ps
    sqlDatabase = db_nm

# -Web Server -Enable
ws_en = settingsStr[settingsStr.find("ws"):settingsStr.find("\n",settingsStr.find("ws"))]
ws_en = ws_en[ws_en.find("=")+1:]
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("ws"):settingsStr.find("\n",settingsStr.find("ws"))],"")

# Pyodbc Config.
SQL_ATTR_CONNECTION_TIMEOUT = 113
login_timeout = 10
connection_timeout = 10

def prebuild():
    
    #Get Infos.
    
    ### Get Connectivity mode
    output = subprocess.Popen(["ip", "address"],stdout = subprocess.PIPE).communicate()[0]
    output = output.decode("utf-8")
    lines = output.split("\n")
    
    wlines = list()
    elines = list()
    
    for i in range(0,len(lines)):
        if ("wlan" in lines[i]):
            wlines.append(lines[i])
        if ("eth" in lines[i]):
            elines.append(lines[i])
    wlanstr = "\n".join(wlines)
    elanstr = "\n".join(elines)
    if ('inet' in wlanstr):
        txt = "Connected   " + wlanstr[wlanstr.find("inet")+5:wlanstr.find("/",wlanstr.find("inet"))]
        wlanMode = 'h7>' + txt + '</h7'
    else:
        wlanMode = 'h8>Not Connected</h8'
    
    if ('inet' in elanstr):
        txt = "Connected   " + elanstr[elanstr.find("inet")+5:elanstr.find("/",elanstr.find("inet"))]
        lanMode = 'h7>' + txt + '</h7'
    else:
        lanMode = 'h8>Not Connected</h8'
    
    # Check INTERNET Connection
    internet = ""
    if (ws_en == "True"):
        # Get RPi IP in PUBLIC
        publicIP = subprocess.Popen(["curl","ifconfig.me/ip"], stdout = subprocess.PIPE).communicate()[0].decode()
        # Set/Reset LOCALN LED
        if (len(publicIP)<16 and len(publicIP)>6):
            internet = 'h7>Accessible ' + publicIP + '</h7'
        else:
            internet = 'h8>Inaccessible</h8'
    else:
        internet = 'h8>Inaccessible</h8'
    ### Get Servers ping
    if (db_en == "True"):
        output = subprocess.Popen(["ping","-w","1","-c","1",db_ip],stdout = subprocess.PIPE).communicate()[0]
        output = output.decode("utf-8")
        if ('100% packet loss' in output or 'unreachable' in output):
            mainServer = 'h8>Offline</h8'
        else:
            mainServer = 'h7>Online</h7'
    else:
        mainServer = 'h8>Disabled Feature</h8'
    
    results_ = ""
    if (db_en == "True"):
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
    dbMode = ""
    if (len(results_)>1):
        dbMode = 'h7>Has Access</h7'
    else:
        dbMode = 'h8>Not Available</h8'
    
    
    ###Get system Uptime
    output = subprocess.Popen(["uptime"],stdout = subprocess.PIPE).communicate()[0]
    uptime = output.decode("utf-8")
    uptime = uptime[:uptime.find("load")]
    uptimeMode = 'h7>'+ uptime + '</h7'
    
    ##############
    
    ###Get system Temp.
    output = subprocess.Popen(["cat", "/sys/devices/virtual/thermal/thermal_zone0/temp"],stdout = subprocess.PIPE).communicate()[0]
    temp = output#.decode("utf-8")
    #temp = temp[5:]
    cpuTemp = 'h7>'+ str(int(temp)/1000.0)+ " 'C" + '</h7'
    
    ##############
    
    ###Get CPU Load Average
    output = subprocess.Popen(["uptime"],stdout = subprocess.PIPE).communicate()[0]
    cpuLoad = output.decode("utf-8")
    cpuLoad = cpuLoad[cpuLoad.find("load")+14:]
    cpuPercents = cpuLoad
    cpuLoad  = "last &nbsp1 min: " + cpuPercents[:4] #str(float(cpuPercents[:4])*100.0) + "%"
    cpuLoad += "<br>last &nbsp5 min: " + cpuPercents[6:10] #str(float(cpuPercents[6:10])*100.0) + "%"
    cpuLoad += "<br>last 15 min: " + cpuPercents[12:17] #str(float(cpuPercents[13:17])*100.0) + "%"
    cpuLoad = 'h7>'+ cpuLoad + '</h7'
    
    ##############
    
    ###Get System INFO.
    cpuInfo = str(psutil.cpu_percent(interval=None))
    cpuInfo = "<h8> USE: " + cpuInfo + "%</h8>&nbsp&nbsp&nbsp&nbsp" + "<h7> IDLE: " + str(100.0-float(cpuInfo)) + "%</h7>"
    
    ramInfo = str(psutil.virtual_memory().percent)
    ramInfo = "<h8> USE: " + ramInfo + "%</h8>&nbsp&nbsp&nbsp&nbsp" + "<h7> IDLE: " + str(100.0-float(ramInfo)) + "%</h7>"
    
    ##############
    ### Main Page Script for Status (when user click on Status Button)
    html_txt  = '\n'
    html_txt  += '\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
    html_txt  += '\n<title>'+co_nm+'</title>'
    #html_txt  += '\n<meta http-equiv="refresh" content="30">'
    html_txt  += '\n<meta name="keywords" content="" />'
    html_txt  += '\n<meta name="description" content="" />'
    html_txt  += '\n<link href="http://'+ipaddr+'/status.css" rel="stylesheet" type="text/css" media="all" />'
    html_txt  += '\n<link href="http://'+ipaddr+'/fonts.css" rel="stylesheet" type="text/css" media="all" />'
    html_txt  += '\n</head>'
    html_txt  += '\n<body>'
    html_txt  += '\n<form method=POST action="events.py">'
    html_txt  += '\n<div id="logo" class="container">'
    html_txt  += '\n	<h1><span class="icon icon-tag icon-size"></span><a>Fire & Smoke <span>Detector</span></a></h1>'
    html_txt  += '\n	<p>'+co_nm+'</a></p></div>'
    html_txt  += '\n	<div class="container"><div class="buttonjustify">'
    html_txt  += '\n	<input type="submit" value="LIVE CAMERA" formaction="liveCamera.py" class="button">'
    html_txt  += '\n <input type=button value="Back" onclick=\'goBack();\' class="button"></div></div><br><br>'
    html_txt  += '\n     <script>'
    html_txt  += '\n function goBack() {'
    html_txt  += '\n   window.history.back()'
    html_txt  += '\n }'
    html_txt  += '\n </script>'
    html_txt  += '\n<div id="wrapper" class="container">'
    html_txt  += '\n	<div id="menu" class="container">'
    html_txt  += '\n		<ul>'
    html_txt  += '\n			<li class="current_page_item"></li>'
    html_txt  += '\n			<li><a accesskey="1" title="">Network Connections</a></li>'
    html_txt  += '\n		</ul>'
    html_txt  += '\n	</div>'
    html_txt  += '\n	<div id="three-column" class="container">'
    html_txt  += '\n		<div id="tbox1"><div class="title">	'
    html_txt  += '\n <p><h9>Wlan:  </h9><'+wlanMode+'></p><br>'
    html_txt  += '\n <p><h9>Eth :  </h9><'+lanMode+'></p><br>'
    html_txt  += '\n <p><h9>Internet :  </h9><'+internet+'></p>'
    html_txt  += '\n	</div></div></div></div>'
    html_txt  += '\n<div id="wrapper" class="container">'
    html_txt  += '\n	<div id="menu" class="container">'
    html_txt  += '\n		<ul>'
    html_txt  += '\n			<li class="current_page_item"></li>'
    html_txt  += '\n			<li><a accesskey="1" title="">Server Status</a></li>'
    html_txt  += '\n		</ul>'
    html_txt  += '\n	</div>'
    html_txt  += '\n	<div id="three-column" class="container">'
    html_txt  += '\n		<div id="tbox1"><div class="title">	'
    html_txt  += '\n <p><h9>Local Server:  </h9><'+mainServer+'></p><br>'
    html_txt  += '\n <p><h9>DataBase:  </h9><'+dbMode+'></p>'
    html_txt  += '\n	</div></div></div></div>'
    html_txt  += '\n<div id="wrapper" class="container">'
    html_txt  += '\n	<div id="menu" class="container">'
    html_txt  += '\n		<ul>'
    html_txt  += '\n			<li class="current_page_item"></li>'
    html_txt  += '\n			<li><a accesskey="1" title="">System Status</a></li>'
    html_txt  += '\n		</ul>'
    html_txt  += '\n	</div>'
    html_txt  += '\n	<div id="three-column" class="container">'
    html_txt  += '\n		<div id="tbox1"><div class="title">	'
    html_txt  += '\n <p><h9>System Uptime:  </h9><br><'+uptimeMode+'>'
    html_txt  += '\n <br><p><h9>CPU Temperature:  </h9><br><'+cpuTemp+'>'
    html_txt  += '\n <br><p><h9>CPU Load Average:  </h9><br><'+cpuLoad+'>'
    html_txt  += '\n <br><p><h9>CPU Usage:  </h9><br>'+cpuInfo
    html_txt  += '\n <br><p><h9>RAM Usage:  </h9><br>'+ramInfo
    html_txt  += '\n	</div></div></div>'
    html_txt  += '\n		</div>'
    html_txt  += '\n	<div id="menu" class="container">'
    html_txt  += '\n		<ul>'
    html_txt  += '\n		</ul><br><br>'
    html_txt  += '\n	</div>'
    html_txt  += '\n	<div id="menu" class="container">'
    html_txt  += '\n		<ul>'
    html_txt  += '\n			<input type="submit" value="Events" class="button"></li>'
    html_txt  += '\n		</ul><br><br>'
    html_txt  += '\n	</div>'
    html_txt  += '\n<div id="copyright">'
    html_txt  += '\n	<p>&copy;All rights reserved. | Designed by IstaSanat +98-914-400-2264<br><a>Firmware version: '+fr_vr+'</a></p>'
    html_txt  += '\n</div>'
    html_txt  += '\n<input type=text value='+si_us+' name="si_us" id="si_us_" class="inputLine" hidden>'
    html_txt  += '\n<input type=text value='+si_ps+' name="si_ps" id="si_ps_" class="inputLine" hidden>'
    html_txt  += '\n</body>'
    html_txt  += '\n</form>'
    html_txt  += '\n</html>'
    
    return html_txt



### Error Page Script (when user and pass are NOT correct)

html_error  = '\n<head>'
html_error  += '\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
html_error  += '\n<title>'+co_nm+'</title>'
html_error  += '\n<meta name="keywords" content="" />'
html_error  += '\n<meta name="description" content="" />'
html_error  += '\n<link href="http://'+ipaddr+'/signin.css" rel="stylesheet" type="text/css" media="all" />'
html_error  += '\n<link href="http://'+ipaddr+'/fonts.css" rel="stylesheet" type="text/css" media="all" />'
html_error  += '\n</head>'
html_error  += '\n<body>'
html_error  += '\n<form>'
html_error  += '\n<div id="logo" class="container">'
html_error  += '\n	<h1><span class="icon icon-lock icon-size"></span><a>Fire & Smoke <span>Detector</span></a></h1>'
html_error  += '\n	<p>'+co_nm+'</a></p></div>'
html_error  += '\n</div>'
html_error  += '\n<div id="wrapper" class="container">'
html_error  += '\n	<div id="menu" class="container">'
html_error  += '\n		<ul>'
html_error  += '\n			<li class="current_page_item"></li>'
html_error  += '\n			<li><a accesskey="1" title="">Loading ERROR !!!</a></li>'
html_error  += '\n		</ul>'
html_error  += '\n	</div>'
html_error  += '\n	<div id="three-column" class="container">'
html_error  += '\n		<div><span class="arrow-down"></span></div>'
html_error  += '\n		<div id="tbox1"><span class="icon icon-exclamation-sign"></span>'
html_error  += '\n		    </div>'
html_error  += '\n		<div id="tbox2">'
html_error  += '\n			<div class="title">'
html_error  += '\n			<h3>Login First, then Try this Page</h3></div>'
html_error  += '\n			<input type=button value="Back to Login Page" onclick=\'window.location.href="http://'+ipaddr+'"\' class="button">'
html_error  += '\n        </div>'
html_error  += '\n	</div>'
html_error  += '\n</div>'
html_error  += '\n<div id="copyright">'
html_error  += '\n	<p>&copy;All rights reserved. | Designed by IstaSanat +98-914-400-2264</a><br><a>Firmware version: '+fr_vr+'</a></a></p>'
html_error  += '\n</div>'
html_error  += '\n</body>'
html_error  += '\n</form>'
html_error  += '\n</html>'

try:
    # Check entered Username and Password
	if (si_us == sius):
		if(si_ps == sips):
			# Show Results in HTML page
			print('Content-type: text/html\n')
			print(prebuild())
		else:
			raise IOERROR
	else:
		raise IOERROR

except:
	#show results in HTML page
	print('Content-type: text/html\n')
	print(html_error)
