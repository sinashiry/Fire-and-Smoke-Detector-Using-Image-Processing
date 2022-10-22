#!/usr/bin/python
# -*- coding: utf-8 -*-

#####################################################
#    Project:     Fire & Smoke Detection            #
#    Designer:    Hossein AalamShahi                #
#    Programmer:  Sina Shiri                        #
#    Date:        2019 Jul 26                       #
#    For:         Ista Sanat Co.                    #
#    File:        Control Panel (Signin Page)       #
#####################################################


import subprocess
from cryptography.fernet import Fernet

output = subprocess.Popen(["hostname","-I"],stdout = subprocess.PIPE).communicate()[0]
if (len(output)>15):
    output = output[:output.find(" ")]
else:
    output = output[:-2]

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

# -Company -Name
co_nm = settingsStr[settingsStr.find("co"):settingsStr.find("\n",settingsStr.find("co"))]
co_nm = co_nm[co_nm.find("=")+1:]
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("co"):settingsStr.find("\n",settingsStr.find("co"))],"")

# -Firmware -Version
fr_vr = settingsStr[settingsStr.find("fr"):settingsStr.find("\n",settingsStr.find("fr"))]
fr_vr = fr_vr[fr_vr.find("=")+1:]
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("fr"):settingsStr.find("\n",settingsStr.find("fr"))],"")


html_txt  = '\n<head>'
html_txt  += '\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
html_txt  += '\n<title>'+co_nm+'</title>'
html_txt  += '\n<meta name="keywords" content="" />'
html_txt  += '\n<meta name="description" content="" />'
html_txt  += '\n  <link rel="stylesheet" href="http://'+output+'/events/bootstrap.min.css">'
html_txt  += '\n<link href="http://'+output+'/signin.css" rel="stylesheet" type="text/css" media="all" />'
html_txt  += '\n<link href="http://'+output+'/fonts.css" rel="stylesheet" type="text/css" media="all" />'

html_txt  += '\n  <script src="http://'+output+'/events/jquery.min.js"></script>'
html_txt  += '\n  <script src="http://'+output+'/events/bootstrap.min.js"></script>'
html_txt  += '\n</head>'
html_txt  += '\n<body>'
html_txt  += '\n<form method=POST action="start.py">'
html_txt  += '\n<div id="logo" class="container">'
html_txt  += '\n	<h1><span class="icon icon-lock icon-size"></span><a>Fire & Smoke <span>Detector</span></a></h1>'
html_txt  += '\n	<p>'+co_nm+'</a></p></div>'
html_txt  += '\n</div>'
html_txt  += '\n<div class="container">'
html_txt  += '\n <input type=button value="About US" data-toggle="modal" data-target="#myModal" class="button">'
html_txt  += '\n  <div class="modal fade" id="myModal" role="dialog">'
html_txt  += '\n    <div class="modal-dialog">'
html_txt  += '\n      <div class="modal-content">'
html_txt  += '\n        <div class="modal-header">'
html_txt  += '\n          <button type="button" class="close" data-dismiss="modal">&times;</button>'
html_txt  += '\n          <h4 class="modal-title">About US</h4>'
html_txt  += '\n       </div>'
html_txt  += '\n        <div class="modal-body">'
html_txt  += '\n          <p>DESIGNED BY ISTASANAT<br>Project:     Fire & Smoke Detection<br>Designer:    Hossein Aalam Shahi<br>Programmer:  Sina Shiri</p>'
html_txt  += '\n        </div>'
html_txt  += '\n        <div class="modal-footer">'
html_txt  += '\n          <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>'
html_txt  += '\n        </div>'
html_txt  += '\n      </div>'
html_txt  += '\n    </div>'
html_txt  += '\n  </div>'
html_txt  += '\n</div>'
html_txt  += '\n<br><br><div id="wrapper" class="container">'
html_txt  += '\n	<div id="menu" class="container">'
html_txt  += '\n		<ul>'
html_txt  += '\n			<li class="current_page_item"></li>'
html_txt  += '\n			<li><a accesskey="1" title="">Login to Settings</a></li>'
html_txt  += '\n		</ul>'
html_txt  += '\n	</div>'
html_txt  += '\n	<div id="three-column" class="container">'
html_txt  += '\n		<div><span class="arrow-down"></span></div>'
html_txt  += '\n		<div id="tbox1"><span class="icon icon-signin"></span>'
html_txt  += '\n		    </div>'
html_txt  += '\n		<div id="tbox2">'
html_txt  += '\n			<div class="title">'
html_txt  += '\n			<h9>Username:</h9> <input type=text name=username class="inputLine">'
html_txt  += '\n			<br><br>'
html_txt  += '\n			<h9>Password:</h9> <input type=password name=password id="pass" class="inputLine">'
html_txt  += '\n        <input type="checkbox" onclick="showPass()">Show'
html_txt  += '\n			'
html_txt  += '\n<script>'
html_txt  += '\nfunction showPass() {'
html_txt  += '\n  var x = document.getElementById("pass");'
html_txt  += '\n  if (x.type === "password") {'
html_txt  += '\n    x.type = "text";'
html_txt  += '\n  } else {'
html_txt  += '\n    x.type = "password";'
html_txt  += '\n  }'
html_txt  += '\n}'
html_txt  += '\n</script>'
html_txt  += '\n			<input type="submit" value="Login" class="button">'
html_txt  += '\n        </div>  </div>'
html_txt  += '\n	</div>'
html_txt  += '\n</div>'
html_txt  += '\n<div id="copyright">'
html_txt  += '\n	<p>&copy;All rights reserved. | Designed by IstaSanat</a><br><a>Firmware version: '+fr_vr+'</a>.</p>'
html_txt  += '\n</div>'
html_txt  += '\n</body>'
html_txt  += '\n</form>'
html_txt  += '\n</html>'

print('Content-type: text/html\n')
print(html_txt)
