#!/usr/bin/python
# -*- coding: utf-8 -*-

#####################################################
#    Project:     Fire & Smoke Detection            #
#    Designer:    Hossein AalamShahi                #
#    Programmer:  Sina Shiri                        #
#    Date:        2019 Aug 03                       #
#    For:         Ista Sanat Co.                    #
#    File:        ControlPanel (Live Camera Page)   #
#####################################################

# Add Needed Modules
from cryptography.fernet import Fernet
import os
import subprocess
import time
import cgi

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


def prebuild():
    ### Main Page Script for Status (when user click on Status Button)
    html_txt  = '\n'
    html_txt  += '\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
    html_txt  += '\n<title>'+co_nm+'</title>'
    html_txt  += '\n<meta name="keywords" content="" />'
    html_txt  += '\n<meta name="description" content="" />'
    html_txt  += '\n<link href="http://'+ipaddr+'/liveCamera.css" rel="stylesheet" type="text/css" media="all" />'
    html_txt  += '\n<link href="http://'+ipaddr+'/fonts.css" rel="stylesheet" type="text/css" media="all" />'
    html_txt  += '\n</head>'
    html_txt  += '\n<body>'
    html_txt  += '\n<form>'
    html_txt  += '\n<div id="logo" class="container">'
    html_txt  += '\n	<h1><span class="icon icon-tag icon-size"></span><a>Fire & Smoke <span>Detector</span></a></h1>'
    html_txt  += '\n	<p>'+co_nm+'</a></p></div>'
    html_txt  += '\n	<div class="container"><div class="buttonjustify">'
    html_txt  += '\n	<input type="button" value="Refresh" onClick="window.location.reload();" class="button">'
    html_txt  += '\n <input type=button value="Back" onclick=\'goBack();\' class="button"></div></div><br><br>'
    html_txt  += '\n     <script>'
    html_txt  += '\n function goBack() {'
    html_txt  += '\n   window.history.back()'
    html_txt  += '\n }'
    html_txt  += '\n </script>'
    html_txt  += '\n<script>' 
    html_txt  += '\nfunction updateImage() {'
    html_txt  += '\n	obj = document.streamFrame;' 
    html_txt  += '\n	obj.src = obj.src.split("?")[0] + "?" + new Date().getTime();' 
    html_txt  += '\n    setTimeout("updateImage()",300);'
    html_txt  += '\n};'
    html_txt  += '\nsetTimeout("updateImage()",300);'
    html_txt  += '\n</script>'
    html_txt  += '\n<div id="wrapper" class="container">'
    html_txt  += '\n	<div id="menu" class="container">'
    html_txt  += '\n		<ul>'
    html_txt  += '\n			<li class="current_page_item"></li>'
    html_txt  += '\n			<li><a accesskey="1" title="">STREAM CAMERA</a></li>'
    html_txt  += '\n		</ul>'
    html_txt  += '\n	</div>'
    html_txt  += '\n	<div id="three-column" class="container"><br><br><br>'
    html_txt  += '\n<img name="streamFrame" src="http://'+ipaddr+'/DB/frame.jpg" style="display: block; margin-left: auto;margin-right: auto;"> '
    html_txt  += '\n	</div></div>'
    html_txt  += '\n	<div id="menu" class="container">'
    html_txt  += '\n	</div>'
    html_txt  += '\n<div id="copyright">'
    html_txt  += '\n	<p>&copy;All rights reserved. | Designed by IstaSanat +98-914-400-2264<br><a>Firmware version: '+fr_vr+'</a></p>'
    html_txt  += '\n</div>'
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
