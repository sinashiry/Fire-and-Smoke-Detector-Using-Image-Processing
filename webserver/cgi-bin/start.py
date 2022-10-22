#!/usr/bin/python
# -*- coding: utf-8 -*-

#####################################################
#    Project:     Fire & Smoke Detection            #
#    Designer:    Hossein AalamShahi                #
#    Programmer:  Sina Shiri                        #
#    Date:        2019 Jul 26                       #
#    For:         Ista Sanat Co.                    #
#    File:        ControlPanel (Start Page)         #
#####################################################


# Add Needed Modules
from cryptography.fernet import Fernet
import os
import subprocess
import time
import cgi

output = subprocess.Popen(["hostname","-I"],stdout = subprocess.PIPE).communicate()[0]
if (len(output)>15):
    output = output[:output.find(" ")]
else:
    output = output[:-2]


#Get Prev. Page Values
form = cgi.FieldStorage()

sius = form.getvalue('username')
sips = form.getvalue('password')


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


# -Zone -Name
zn_nm = settingsStr[settingsStr.find("zn"):settingsStr.find("\n",settingsStr.find("zn"))]
zn_nm = zn_nm[zn_nm.find("=")+1:]
zn_nm = zn_nm.replace('"','&quot;')
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("zn"):settingsStr.find("\n",settingsStr.find("zn"))],"")

# -Zone -Mode
zn_md = settingsStr[settingsStr.find("zn"):settingsStr.find("\n",settingsStr.find("zn"))]
zn_md = zn_md[zn_md.find("=")+1:]
zn_md = zn_md.replace('"','&quot;')
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("zn"):settingsStr.find("\n",settingsStr.find("zn"))],"")


# -SMS -Enable
sm_en = settingsStr[settingsStr.find("sm"):settingsStr.find("\n",settingsStr.find("sm"))]
sm_en = sm_en[sm_en.find("=")+1:]
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("sm"):settingsStr.find("\n",settingsStr.find("sm"))],"")

# -SMS -Number(s)
sm_pn = settingsStr[settingsStr.find("sm"):settingsStr.find("\n",settingsStr.find("sm"))]
sm_pn = sm_pn[sm_pn.find("=")+1:]
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("sm"):settingsStr.find("\n",settingsStr.find("sm"))],"")
sm_pn_list = list()
sm_pn_list = sm_pn.split(",")


# -GSM -Enable
gs_en = settingsStr[settingsStr.find("gs"):settingsStr.find("\n",settingsStr.find("gs"))]
gs_en = gs_en[gs_en.find("=")+1:]
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("gs"):settingsStr.find("\n",settingsStr.find("gs"))],"")

# -GSM -APN
gs_ap = settingsStr[settingsStr.find("gs"):settingsStr.find("\n",settingsStr.find("gs"))]
gs_ap = gs_ap[gs_ap.find("=")+1:]
gs_ap = gs_ap.replace('"','&quot;')
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("gs"):settingsStr.find("\n",settingsStr.find("gs"))],"")


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


# -Web SERVER -Enable
ws_en = settingsStr[settingsStr.find("ws"):settingsStr.find("\n",settingsStr.find("ws"))]
ws_en = ws_en[ws_en.find("=")+1:]
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("ws"):settingsStr.find("\n",settingsStr.find("ws"))],"")

# -Web SERVER -Address
ws_ad = settingsStr[settingsStr.find("ws"):settingsStr.find("\n",settingsStr.find("ws"))]
ws_ad = ws_ad[ws_ad.find("=")+1:]
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("ws"):settingsStr.find("\n",settingsStr.find("ws"))],"")

# -Web SERVER -URL
ws_ul = settingsStr[settingsStr.find("ws"):settingsStr.find("\n",settingsStr.find("ws"))]
ws_ul = ws_ul[ws_ul.find("=")+1:]
ws_ul = ws_ul.replace('"','&quot;')
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
fp_us = fp_us.replace('"','&quot;')
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("fp"):settingsStr.find("\n",settingsStr.find("fp"))],"")

# -FTP SERVER -Password
fp_ps = settingsStr[settingsStr.find("fp"):settingsStr.find("\n",settingsStr.find("fp"))]
fp_ps = fp_ps[fp_ps.find("=")+1:]
fp_ps = fp_ps.replace('"','&quot;')
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("fp"):settingsStr.find("\n",settingsStr.find("fp"))],"")


# -WiFi -Enable
wi_en = settingsStr[settingsStr.find("wi"):settingsStr.find("\n",settingsStr.find("wi"))]
wi_en = wi_en[wi_en.find("=")+1:]
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("wi"):settingsStr.find("\n",settingsStr.find("wi"))],"")

# -WiFi -SSID
wi_nm = settingsStr[settingsStr.find("wi"):settingsStr.find("\n",settingsStr.find("wi"))]
wi_nm = wi_nm[wi_nm.find("=")+1:]
wi_nm = wi_nm.replace('"','&quot;')
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("wi"):settingsStr.find("\n",settingsStr.find("wi"))],"")

# -WiFi -Password
wi_ps = settingsStr[settingsStr.find("wi"):settingsStr.find("\n",settingsStr.find("wi"))]
wi_ps = wi_ps[wi_ps.find("=")+1:]
wi_ps = wi_ps.replace('"','&quot;')
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("wi"):settingsStr.find("\n",settingsStr.find("wi"))],"")

# -Pre-Alarm -Enable
pa_en = settingsStr[settingsStr.find("pa"):settingsStr.find("\n",settingsStr.find("pa"))]
pa_en = pa_en[pa_en.find("=")+1:]
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("pa"):settingsStr.find("\n",settingsStr.find("pa"))],"")

# -Alarm -Enable
al_en = settingsStr[settingsStr.find("al"):settingsStr.find("\n",settingsStr.find("al"))]
al_en = al_en[al_en.find("=")+1:]
settingsStr = settingsStr.replace(settingsStr[settingsStr.find("al"):settingsStr.find("\n",settingsStr.find("al"))],"")


paEn = ""
paDi = ""
if (pa_en == 'True'):
    paEn = "selected"
else:
    paDi = "selected"

alEn = ""
alDi = ""
if (al_en == 'True'):
    alEn = "selected"
else:
    alDi = "selected"
    
smEn = ""
smDi = ""
if (sm_en == 'True'):
    smEn = "selected"
else:
    smDi = "selected"

dbEn = ""
dbDi = ""
if (db_en == 'True'):
    dbEn = "selected"
else:
    dbDi = "selected"

wsEn = ""
wsDi = ""
if (ws_en == 'True'):
    wsEn = "selected"
else:
    wsDi = "selected"
    
gsEn = ""
gsDi = ""
if (gs_en == 'True'):
    gsEn = "selected"
else:
    gsDi = "selected"

wiEn = ""
wiDi = ""
if (wi_en == 'True'):
    wiEn = "selected"
else:
    wiDi = "selected"


### Main Page Script for Settings (when user and pass are correct)

html_txt  = '\n'
html_txt  += '\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
html_txt  += '\n<title>'+co_nm+'</title>'
html_txt  += '\n<meta name="keywords" content="" />'
html_txt  += '\n<meta name="description" content="" />'
html_txt  += '\n<link href="http://'+output+'/start.css" rel="stylesheet" type="text/css" media="all" />'
html_txt  += '\n<link href="http://'+output+'/fonts.css" rel="stylesheet" type="text/css" media="all" />'
html_txt  += '\n</head>'
html_txt  += '\n<body>'
html_txt  += '\n<form method=POST action="reboot.py">'
html_txt  += '\n<div id="logo" class="container">'
html_txt  += '\n	<h1><span class="icon icon-tags icon-size"></span><a>Fire & Smoke <span>Detector</span></a></h1>'
html_txt  += '\n	<p>'+co_nm+'</a></p></div>'
html_txt  += '\n	<div class="container"><div class="buttonjustify"><input type="button" value="Factory Defaults" onclick="setdefault();" class="button">'
html_txt  += '\n <input type=button value="Logout" onclick=\'window.location.href="http://'+output+'"\' class="button"></div>'
html_txt  += '\n <input type="submit" value="Status" formaction="status.py" class="button"></div><br><br>'
html_txt  += '\n<div id="wrapper" class="container">'

# Zone Settings
html_txt  += '\n	<div id="menu" class="container">'
html_txt  += '\n		<ul>'
html_txt  += '\n			<li class="current_page_item"></li>'
html_txt  += '\n			<li><a accesskey="1" title="">Zone Settings</a></li>'
html_txt  += '\n		</ul>'
html_txt  += '\n	</div>'
html_txt  += '\n	<div id="three-column" class="container">'
html_txt  += '\n		<div id="tbox1"><div class="title">	'
html_txt  += '\n 		<h9>Zone Name:  </h9><input type=text size="20" value="' + zn_nm
html_txt  += '" name=zn_nm id="zn_nm_" class="inputLine">'
html_txt  += '\n 		<br><h9>Zone Type:  </h9><input type=text size="20" value="' + zn_md
html_txt  += '" name=zn_md id="zn_md_" class="inputLine">'
html_txt  += '\n	</div></div>'
html_txt  += '\n	</div>'
#####################

# Alarm Settings
html_txt  += '\n	<div id="menu" class="container">'
html_txt  += '\n		<ul>'
html_txt  += '\n			<li class="current_page_item"></li>'
html_txt  += '\n			<li><a accesskey="1" title="">Emergency Alarm Settings</a></li>'
html_txt  += '\n		</ul>'
html_txt  += '\n	</div>'
html_txt  += '\n	<div id="three-column" class="container">'
html_txt  += '\n		<div id="tbox1"><div class="title">'
html_txt  += '\n  <h9>Pre-Alarm Output:</h9>'
html_txt  += '\n  <select name=pa_en id="pa_en_" class="inputLine">'
html_txt  += '\n  <option value="True" '+paEn+'>Enable</option>'
html_txt  += '\n  <option value="False" '+paDi+'>Disable</option>'
html_txt  += '\n  </select>'
html_txt  += '\n  <br><h9>Alarm Output:</h9>'
html_txt  += '\n  <select name=al_en id="al_en_" class="inputLine">'
html_txt  += '\n  <option value="True" '+alEn+'>Enable</option>'
html_txt  += '\n  <option value="False" '+alDi+'>Disable</option>'
html_txt  += '\n  </select>'
html_txt  += '\n	</div></div>'
html_txt  += '\n	</div>'
#####################

# SMS Settings
html_txt  += '\n	<div id="menu" class="container">'
html_txt  += '\n		<ul>'
html_txt  += '\n			<li class="current_page_item"></li>'
html_txt  += '\n			<li><a accesskey="1" title="">SMS Settings</a></li>'
html_txt  += '\n		</ul>'
html_txt  += '\n	</div>'
html_txt  += '\n	<div id="three-column" class="container">'
html_txt  += '\n		<div id="tbox1"><div class="title">'
html_txt  += '\n  <h9>SMS Output:</h9>'
html_txt  += '\n  <select name=sm_en id="sm_en_" class="inputLine" onchange="changeSMSMode()">'
html_txt  += '\n  <option value="True" '+smEn+'>Enable</option>'
html_txt  += '\n  <option value="False" '+smDi+'>Disable</option>'
html_txt  += '\n  </select>'

# Get each Phone Number(s)
pn_1 = ""; pn_2 = ""; pn_3 = ""
pn_1_CH = ""; pn_2_CH = ""; pn_3_CH = ""
for i in range(0,len(sm_pn_list)):
    if i==0:
        if (sm_pn_list[0].find("*") != -1):
            pn_1_CH = "checked"
            sm_pn_list[0] = sm_pn_list[0].replace("*","")
        pn_1 = sm_pn_list[0]
    if i==1:
        if (sm_pn_list[1].find("*") != -1):
            pn_2_CH = "checked"
            sm_pn_list[1] = sm_pn_list[1].replace("*","")
        pn_2 = sm_pn_list[1]
    if i==2:
        if (sm_pn_list[2].find("*") != -1):
            pn_3_CH = "checked"
            sm_pn_list[2] = sm_pn_list[2].replace("*","")
        pn_3 = sm_pn_list[2]

html_txt  += '\n<table style="width:100%" id="sm_tb_">'
html_txt  += '\n  <tr><th align="left">'
html_txt  += '\n 		<br><br><h9 id="pn_header">Phone Numbers:  </h9><br><input type=text value="' + pn_1
html_txt  += '" name=pn_1 id="pn_1_" class="inputLine" maxlength="13"'
html_txt  += ' onkeypress="return event.charCode >= 48 && event.charCode <= 57 || event.charCode <= 43">'
html_txt  += '\n        <input name=pn_1_ch id="pn_1_ch_" type="checkbox" '+pn_1_CH+'>Send'
html_txt  += '\n 		<br><input type=text value="' + pn_2
html_txt  += '" name=pn_2 id="pn_2_" class="inputLine" maxlength="13"'
html_txt  += ' onkeypress="return event.charCode >= 48 && event.charCode <= 57 || event.charCode <= 43">'
html_txt  += '\n        <input name=pn_2_ch id="pn_2_ch_" type="checkbox" '+pn_2_CH+'>Send'
html_txt  += '\n 		<br><input type=text value="' + pn_3
html_txt  += '" name=pn_3 id="pn_3_" class="inputLine" maxlength="13"'
html_txt  += ' onkeypress="return event.charCode >= 48 && event.charCode <= 57 || event.charCode <= 43">'
html_txt  += '\n        <input name=pn_3_ch id="pn_3_ch_" type="checkbox" '+pn_3_CH+'>Send'
html_txt  += '\n  </th></tr>'
html_txt  += '\n</table>'
html_txt  += '\n	</div></div>'
html_txt  += '\n	</div>'

# JS Script for this section
html_txt  += '\n <script>'
html_txt  += '\n var sm_en_field = document.getElementById("sm_en_");'
html_txt  += '\n if (sm_en_field.value == "True") {'
html_txt  += '\n    sm_tb_.style.display = \'block\';'
html_txt  += '\n } else {'
html_txt  += '\n    sm_tb_.style.display = \'none\';'
html_txt  += '\n }'
html_txt  += '\n </script>'
html_txt  += '\n <script>'
html_txt  += '\n function changeSMSMode(){'
html_txt  += '\n    var sm_en_field = document.getElementById("sm_en_");'
html_txt  += '\n    if (sm_en_field.value == "True") {'
html_txt  += '\n        sm_tb_.style.display = \'block\';'
html_txt  += '\n    } else {'
html_txt  += '\n        sm_tb_.style.display = \'none\';'
html_txt  += '\n    }'
html_txt  += '\n }'
html_txt  += '\n </script>'
#####################

# Local DataBase
html_txt  += '\n	<div id="menu" class="container">'
html_txt  += '\n		<ul>'
html_txt  += '\n			<li class="current_page_item"></li>'
html_txt  += '\n			<li><a accesskey="1" title="">Local SQL Server Database Settings</a></li>'
html_txt  += '\n		</ul>'
html_txt  += '\n	</div>'
html_txt  += '\n	<div id="three-column" class="container">'
html_txt  += '\n		<div id="tbox1"><div class="title">'
html_txt  += '\n  <h9>Local DataBase Output:</h9>'
html_txt  += '\n  <select name=db_en id="db_en_" class="inputLine" onchange="changeDBMode()">'
html_txt  += '\n  <option value="True" '+dbEn+'>Enable</option>'
html_txt  += '\n  <option value="False" '+dbDi+'>Disable</option>'
html_txt  += '\n  </select>'
html_txt  += '\n<table style="width:100%" id="db_tb_">'
html_txt  += '\n  <tr><th align="left">'
html_txt  += '\n <br><h9>Server IP:  </h9><input type=text value="'
html_txt  += db_ip[0:db_ip.find(".")]
db_ip = db_ip[db_ip.find(".") + 1:]
html_txt  += '" name=db_ip1 id="db_ip1_" size="3" maxlength="3"'
html_txt  += ' onkeypress="return event.charCode >= 48 && event.charCode <= 57" class="inputLine">\n'
html_txt  += '. <input type=text value="'
html_txt  += db_ip[0:db_ip.find(".")]
db_ip = db_ip[db_ip.find(".") + 1:]
html_txt  += '" name=db_ip2 id="db_ip2_" size="3" maxlength="3"'
html_txt  += ' onkeypress="return event.charCode >= 48 && event.charCode <= 57" class="inputLine">\n'
html_txt  += ". <input type=text value=\""
html_txt  += db_ip[0:db_ip.find(".")]
db_ip = db_ip[db_ip.find(".") + 1:]
html_txt  += '" name=db_ip3 id="db_ip3_" size="3" maxlength="3"'
html_txt  += ' onkeypress="return event.charCode >= 48 && event.charCode <= 57" class="inputLine">\n'
html_txt  += '. <input type=text value="'
html_txt  += db_ip[0:]
html_txt  += '" name=db_ip4 id="db_ip4_" size="3" maxlength="3"'
html_txt  += ' onkeypress="return event.charCode >= 48 && event.charCode <= 57" class="inputLine">\n'
html_txt  += '<br>'
html_txt  += '\n  <h9>Server Port:  </h9><input type=text value="'
html_txt  += db_pt
html_txt  += '" name=db_pt id="db_pt_" size="4" maxlength="4"'
html_txt  += ' onkeypress="return event.charCode >= 48 && event.charCode <= 57" class="inputLine">\n'
html_txt  += '<br>'
html_txt  += '\n  <h9>Server Username:  </h9><input type=text value="'
html_txt  += db_us
html_txt  += '" name=db_us id="db_us_" size="20" class="inputLine">\n'
html_txt  += '<br>'
html_txt  += '\n  <h9>Server Password: </h9><input type=password value="'
html_txt  += db_ps
html_txt  += '" name=db_ps id="db_ps_" size="20" class="inputLine">\n'
html_txt  += '\n        <input type="checkbox" onclick="showPassdb()">Show'
html_txt  += '<br>'
html_txt  += '\n  <h9>Database Name:  </h9><input type=text value="'
html_txt  += db_nm
html_txt  += '" name=db_nm id="db_nm_" size="20" class="inputLine">\n'
html_txt  += '\n  </th></tr>'
html_txt  += '\n</table>'
html_txt  += '\n		</div></div>'
html_txt  += '\n	</div>'

# JS Script for this section
html_txt  += '\n<script>'
html_txt  += '\nfunction showPassdb() {'
html_txt  += '\n  var x = document.getElementById("db_ps_");'
html_txt  += '\n  if (x.type === "password") {'
html_txt  += '\n    x.type = "text";'
html_txt  += '\n  } else {'
html_txt  += '\n    x.type = "password";'
html_txt  += '\n  }'
html_txt  += '\n}'
html_txt  += '\n</script>'
html_txt  += '\n <script>'
html_txt  += '\n var db_en_field = document.getElementById("db_en_");'
html_txt  += '\n if (db_en_field.value == "True") {'
html_txt  += '\n    db_tb_.style.display = \'block\';'
html_txt  += '\n } else {'
html_txt  += '\n    db_tb_.style.display = \'none\';'
html_txt  += '\n }'
html_txt  += '\n </script>'
html_txt  += '\n <script>'
html_txt  += '\n function changeDBMode(){'
html_txt  += '\n    var db_en_field = document.getElementById("db_en_");'
html_txt  += '\n    if (db_en_field.value == "True") {'
html_txt  += '\n        db_tb_.style.display = \'block\';'
html_txt  += '\n    } else {'
html_txt  += '\n        db_tb_.style.display = \'none\';'
html_txt  += '\n    }'
html_txt  += '\n }'
html_txt  += '\n </script>'
#####################

# Web Server Settings
html_txt  += '\n	<div id="menu" class="container">'
html_txt  += '\n		<ul>'
html_txt  += '\n			<li class="current_page_item"></li>'
html_txt  += '\n			<li><a accesskey="1" title="">Web Server Settings</a></li>'
html_txt  += '\n		</ul>'
html_txt  += '\n	</div>'
html_txt  += '\n	<div id="three-column" class="container">'
html_txt  += '\n		<div id="tbox1"><div class="title">'
html_txt  += '\n  <h9>Web Server Output:</h9>'
html_txt  += '\n  <select name=ws_en id="ws_en_" class="inputLine" onchange="changeWSMode()">'
html_txt  += '\n  <option value="True" '+wsEn+'>Enable</option>'
html_txt  += '\n  <option value="False" '+wsDi+'>Disable</option>'
html_txt  += '\n  </select>'
html_txt  += '<br>'
html_txt  += '\n<table style="width:100%" id="ws_tb_">'
html_txt  += '\n  <tr><th align="left">'
html_txt  += '\n  <br><h9>Server Address:  </h9><input type=text value="'
html_txt  += ws_ad
html_txt  += '" name=ws_ad id="ws_ad_" size="20" class="inputLine">\n'
html_txt  += '<br>'
html_txt  += '\n  <h9>Server Ad. URL:  </h9><input type=text value="'
html_txt  += ws_ul
html_txt  += '" name=ws_ul id="ws_ul_" size="20" class="inputLine">\n'
html_txt  += '<br>'
html_txt  += '\n  <h9>FTP Address:  </h9><input type=text value="'
html_txt  += fp_ad
html_txt  += '" name=fp_ad id="fp_ad_" size="20" class="inputLine">\n'
html_txt  += '<br>'
html_txt  += '\n  <h9>FTP Port:  </h9><input type=text value="'
html_txt  += fp_pt
html_txt  += '" name=fp_pt id="fp_pt_" size="4" class="inputLine" maxlength="4"'
html_txt  += ' onkeypress="return event.charCode >= 48 && event.charCode <= 57" class="inputLine">\n'
html_txt  += '<br>'
html_txt  += '\n  <h9>FTP Username:  </h9><input type=text value="'
html_txt  += fp_us
html_txt  += '" name=fp_us id="fp_us_" size="20" class="inputLine">\n'
html_txt  += '<br>'
html_txt  += '\n  <h9>FTP Password:  </h9><input type=password value="'
html_txt  += fp_ps
html_txt  += '" name=fp_ps id="fp_ps_" size="20" class="inputLine">\n'
html_txt  += '\n        <input type="checkbox" onclick="showPassfp()">Show'
html_txt  += '\n			'
html_txt  += '\n  </th></tr>'
html_txt  += '\n</table>'
html_txt  += '\n		</div></div>'
html_txt  += '\n	</div>'

# JS Script for this section
html_txt  += '\n<script>'
html_txt  += '\nfunction showPassfp() {'
html_txt  += '\n  var x = document.getElementById("fp_ps_");'
html_txt  += '\n  if (x.type === "password") {'
html_txt  += '\n    x.type = "text";'
html_txt  += '\n  } else {'
html_txt  += '\n    x.type = "password";'
html_txt  += '\n  }'
html_txt  += '\n}'
html_txt  += '\n</script>'
html_txt  += '\n <script>'
html_txt  += '\n var ws_en_field = document.getElementById("ws_en_");'
html_txt  += '\n if (ws_en_field.value == "True") {'
html_txt  += '\n    ws_tb_.style.display = \'block\';'
html_txt  += '\n } else {'
html_txt  += '\n    ws_tb_.style.display = \'none\';'
html_txt  += '\n }'
html_txt  += '\n </script>'
html_txt  += '\n <script>'
html_txt  += '\n function changeWSMode(){'
html_txt  += '\n    var ws_en_field = document.getElementById("ws_en_");'
html_txt  += '\n    if (ws_en_field.value == "True") {'
html_txt  += '\n        ws_tb_.style.display = \'block\';'
html_txt  += '\n    } else {'
html_txt  += '\n        ws_tb_.style.display = \'none\';'
html_txt  += '\n    }'
html_txt  += '\n }'
html_txt  += '\n </script>'
#####################

# GSM Settings
html_txt  += '\n	<div id="menu" class="container">'
html_txt  += '\n		<ul>'
html_txt  += '\n			<li class="current_page_item"></li>'
html_txt  += '\n			<li><a accesskey="1" title="">GSM Module Settings</a></li>'
html_txt  += '\n		</ul>'
html_txt  += '\n	</div>'
html_txt  += '\n	<div id="three-column" class="container">'
html_txt  += '\n		<div id="tbox1"><div class="title">'
html_txt  += '\n  <h9>GSM Output:</h9>'
html_txt  += '\n  <select name=gs_en id="gs_en_" class="inputLine" onchange="changeGSMMode()">'
html_txt  += '\n  <option value="True" '+gsEn+'>Enable</option>'
html_txt  += '\n  <option value="False" '+gsDi+'>Disable</option>'
html_txt  += '\n  </select>'
html_txt  += '\n<table style="width:100%" id="gs_tb_">'
html_txt  += '\n  <tr><th align="left">'
html_txt  += '\n 		<br><h9 id="gs_header">GSM APN:  </h9><input type=text value="' + gs_ap
html_txt  += '" name=gs_ap id="gs_ap_" class="inputLine" size="20">'
html_txt  += '\n  </th></tr>'
html_txt  += '\n</table>'
html_txt  += '\n		</div></div>'
html_txt  += '\n	</div>'

# JS Script for this section
html_txt  += '\n <script>'
html_txt  += '\n var gs_en_field = document.getElementById("gs_en_");'
html_txt  += '\n if (gs_en_field.value == "True") {'
html_txt  += '\n    gs_tb_.style.display = \'block\';'
html_txt  += '\n } else {'
html_txt  += '\n    gs_tb_.style.display = \'none\';'
html_txt  += '\n }'
html_txt  += '\n </script>'
html_txt  += '\n <script>'
html_txt  += '\n function changeGSMMode(){'
html_txt  += '\n    var gs_en_field = document.getElementById("gs_en_");'
html_txt  += '\n    if (gs_en_field.value == "True") {'
html_txt  += '\n        gs_tb_.style.display = \'block\';'
html_txt  += '\n    } else {'
html_txt  += '\n        gs_tb_.style.display = \'none\';'
html_txt  += '\n    }'
html_txt  += '\n }'
html_txt  += '\n </script>'
#####################

# WiFi Settings
html_txt  += '\n	<div id="menu" class="container">'
html_txt  += '\n		<ul>'
html_txt  += '\n			<li class="current_page_item"></li>'
html_txt  += '\n			<li><a accesskey="1" title="">WiFi Adapter Settings</a></li>'
html_txt  += '\n		</ul>'
html_txt  += '\n	</div>'
html_txt  += '\n	<div id="three-column" class="container">'
html_txt  += '\n		<div id="tbox1"><div class="title">'
html_txt  += '\n  <h9>WiFi Connection:</h9>'
html_txt  += '\n  <select name=wi_en id="wi_en_" class="inputLine" onchange="changeWiFiMode()">'
html_txt  += '\n  <option value="True" '+wiEn+'>Enable</option>'
html_txt  += '\n  <option value="False" '+wiDi+'>Disable</option>'
html_txt  += '\n  </select>'
html_txt  += '\n<table style="width:100%" id="wi_tb_">'
html_txt  += '\n  <tr><th align="left">'
html_txt  += '\n  <br><h9>SSID Name:  </h9><input type=text value="'
html_txt  += wi_nm
html_txt  += '" name=wi_nm id="wi_nm_" class="inputLine">\n'
html_txt  += '<br><br>'
html_txt  += '\n  <h9>Password:  </h9><input type=password value="'
html_txt  += wi_ps
html_txt  += '" name=wi_ps id="wi_ps_" class="inputLine">\n'
html_txt  += '\n<input type="checkbox" onclick="showwifiPass()">Show'
html_txt  += '\n  </th></tr>'
html_txt  += '\n</table>'
html_txt  += '\n		</div></div>'
html_txt  += '\n	</div>'

# JS Script for this section
html_txt  += '\n<script>'
html_txt  += '\nfunction showwifiPass() {'
html_txt  += '\n  var x = document.getElementById("wi_ps_");'
html_txt  += '\n  if (x.type === "password") {'
html_txt  += '\n    x.type = "text";'
html_txt  += '\n  } else {'
html_txt  += '\n    x.type = "password";'
html_txt  += '\n  }'
html_txt  += '\n}'
html_txt  += '\n</script>'
html_txt  += '\n <script>'
html_txt  += '\n var wi_en_field = document.getElementById("wi_en_");'
html_txt  += '\n if (wi_en_field.value == "True") {'
html_txt  += '\n    wi_tb_.style.display = \'block\';'
html_txt  += '\n } else {'
html_txt  += '\n    wi_tb_.style.display = \'none\';'
html_txt  += '\n }'
html_txt  += '\n </script>'
html_txt  += '\n <script>'
html_txt  += '\n function changeWiFiMode(){'
html_txt  += '\n    var wi_en_field = document.getElementById("wi_en_");'
html_txt  += '\n    if (wi_en_field.value == "True") {'
html_txt  += '\n        wi_tb_.style.display = \'block\';'
html_txt  += '\n    } else {'
html_txt  += '\n        wi_tb_.style.display = \'none\';'
html_txt  += '\n    }'
html_txt  += '\n }'
html_txt  += '\n </script>'
#####################

# Co. name and Firmware Settings
html_txt  += '\n<div id="menu" class="container">'
html_txt  += '\n		<ul>'
html_txt  += '\n			<li class="current_page_item"></li>'
html_txt  += '\n			<li><a accesskey="1" title="">Edit Settings Page Title(s)</a></li>'
html_txt  += '\n		</ul>'
html_txt  += '\n	</div>'
html_txt  += '\n	<div id="three-column" class="container">'
html_txt  += '\n		<div id="tbox1"><div class="title">'
html_txt  += '\n  <h9>Company Name:  </h9><input type=text value="'
html_txt  += co_nm
html_txt  += '" name="co_nm" id="co_nm_" class="inputLine">\n'
html_txt  += '\n  <br><h9>Firmware Version:  </h9><input type=text value="'
html_txt  += fr_vr
html_txt  += '" name="fr_vr" id="fr_vr_" size="10" class="inputLine">\n'
html_txt  += '\n		</div></div>'
html_txt  += '\n	</div>'
#####################

# Login to Control Panel Settings
html_txt  += '\n	<div id="menu" class="container">'
html_txt  += '\n		<ul>'
html_txt  += '\n			<li class="current_page_item"></li>'
html_txt  += '\n			<li><a accesskey="1" title="">Login Settings</a></li>'
html_txt  += '\n		</ul>'
html_txt  += '\n	</div>'
html_txt  += '\n	<div id="three-column" class="container">'
html_txt  += '\n		<div id="tbox1"><div class="title">'
html_txt  += '\n  <h9>Username:  </h9><input type=text value="'
html_txt  += si_us
html_txt  += '" name=si_us id="si_us_" class="inputLine">\n'
html_txt  += '\n<input type="password" value="'
html_txt  += si_ps
html_txt  += '" name=si_ps id="si_ps_" class="inputLine" hidden>\n'
html_txt  += '<br><br><br><br><br><br><br>'
html_txt  += '\n  <h3>If you want to change Login Password, </h3><br>'
html_txt  += '\n  <h3>Put your new password into two fields.  </h3><br>'
html_txt  += '\n  <h9>New Password:  &nbsp&nbsp&nbsp&nbsp&nbsp</h9><input type=password value="'
html_txt  += ''
html_txt  += '" name=nlgp id="newLogPass"  onkeyup="check();" class="inputLine">\n'
html_txt  += '\n<input type="checkbox" onclick="shownewPass()">Show'
html_txt  += '\n  <br><h9>Confirm Password:  </h9><input type=password value="'
html_txt  += ''
html_txt  += '" name=clgp id="conLogPass"  onkeyup="check();" class="inputLine">\n'
html_txt  += '\n<input type="checkbox" onclick="showconPass()">Show'
html_txt  += '\n &nbsp&nbsp&nbsp<h9 id="message"></h9>'
html_txt  += '\n<input type=text name=coms id="conmess" hidden>'
html_txt  += '\n		</div></div>'
html_txt  += '\n	</div>'
html_txt  += '\n</div>'

# JS Script for this section
html_txt  += '\n<script>'
html_txt  += '\nfunction showPass() {'
html_txt  += '\n  var x = document.getElementById("logpass");'
html_txt  += '\n  if (x.type === "password") {'
html_txt  += '\n    x.type = "text";'
html_txt  += '\n  } else {'
html_txt  += '\n    x.type = "password";'
html_txt  += '\n  }'
html_txt  += '\n}'
html_txt  += '\n</script>'
html_txt  += '\n<script>'
html_txt  += '\nfunction shownewPass() {'
html_txt  += '\n  var x = document.getElementById("newLogPass");'
html_txt  += '\n  if (x.type === "password") {'
html_txt  += '\n    x.type = "text";'
html_txt  += '\n  } else {'
html_txt  += '\n    x.type = "password";'
html_txt  += '\n  }'
html_txt  += '\n}'
html_txt  += '\n</script>'
html_txt  += '\n<script>'
html_txt  += '\nfunction showconPass() {'
html_txt  += '\n  var x = document.getElementById("conLogPass");'
html_txt  += '\n  if (x.type === "password") {'
html_txt  += '\n    x.type = "text";'
html_txt  += '\n  } else {'
html_txt  += '\n    x.type = "password";'
html_txt  += '\n  }'
html_txt  += '\n}'
html_txt  += '\n</script>'
html_txt  += '\n<script>'
html_txt  += '\nvar check = function() {'
html_txt  += '\n  if (document.getElementById("newLogPass").value == ""'
html_txt  += '\n    || document.getElementById("conLogPass").value == "") {'
html_txt  += '\n    document.getElementById("conmess").value = "Put password"'
html_txt  += '\n    document.getElementById("message").style.color = "orange";'
html_txt  += '\n    document.getElementById("message").innerHTML = "Put password";}'
html_txt  += '\n  else { if (document.getElementById("newLogPass").value =='
html_txt  += '\n    document.getElementById("conLogPass").value) {'
html_txt  += '\n    document.getElementById("conmess").value = "Matching"'
html_txt  += '\n    document.getElementById("message").style.color = "green";'
html_txt  += '\n    document.getElementById("message").innerHTML = "Matching";'
html_txt  += '\n  } else {'
html_txt  += '\n    document.getElementById("conmess").value = "not matching"'
html_txt  += '\n    document.getElementById("message").style.color = "red";'
html_txt  += '\n    document.getElementById("message").innerHTML = "not matching";'
html_txt  += '\n  }}'
html_txt  += '\n}'
html_txt  += '\n</script>'
html_txt  += '\n	<div id="menu" class="container">'
html_txt  += '\n		<ul>'
html_txt  += '\n			<input type="submit" value="Save & Reboot" class="button"></li>'
html_txt  += '\n		</ul><br><br>'
html_txt  += '\n	</div>'
html_txt  += '\n</form>'
html_txt  += '\n<div id="copyright">'
html_txt  += '\n	<p><a>&copy;All rights reserved. | Designed by IstaSanat +98-914-400-2264</a><br><a>Firmware version: '+fr_vr+'</a></p>'
html_txt  += '\n</div>'
html_txt  += '\n<script>'
html_txt  += '\nfunction setdefault() {'
html_txt  += '\n var answer = confirm("Do you want to set Factory default settings?")'
html_txt  += '\n if (answer) {'
html_txt  += '\n    document.getElementById("zn_nm_").value = "Place One";'
html_txt  += '\n    document.getElementById("zn_md_").value = "Zone 1";'
html_txt  += '\n    document.getElementById("pa_en_").value = "True";'
html_txt  += '\n    document.getElementById("al_en_").value = "True";'
html_txt  += '\n    document.getElementById("sm_en_").value = "False";'
html_txt  += '\n    document.getElementById("pn_1_").value = " ";'
html_txt  += '\n    document.getElementById("pn_2_").value = " ";'
html_txt  += '\n    document.getElementById("pn_3_").value = " ";'
html_txt  += '\n    document.getElementById("pn_1_ch_").checked = false;'
html_txt  += '\n    document.getElementById("pn_2_ch_").checked = false;'
html_txt  += '\n    document.getElementById("pn_3_ch_").checked = false;'
html_txt  += '\n    document.getElementById("db_en_").value = "False";'
html_txt  += '\n    document.getElementById("db_ip1_").value = "0";'
html_txt  += '\n    document.getElementById("db_ip2_").value = "0";'
html_txt  += '\n    document.getElementById("db_ip3_").value = "0";'
html_txt  += '\n    document.getElementById("db_ip4_").value = "0";'
html_txt  += '\n    document.getElementById("db_pt_").value = "1433";'
html_txt  += '\n    document.getElementById("db_us_").value = " ";'
html_txt  += '\n    document.getElementById("db_ps_").value = " ";'
html_txt  += '\n    document.getElementById("db_nm_").value = " ";'
html_txt  += '\n    document.getElementById("ws_en_").value = "False";'
html_txt  += '\n    document.getElementById("ws_ad_").value = " ";'
html_txt  += '\n    document.getElementById("ws_ul_").value = "/";'
html_txt  += '\n    document.getElementById("fp_ad_").value = " ";'
html_txt  += '\n    document.getElementById("fp_pt_").value = " ";'
html_txt  += '\n    document.getElementById("fp_us_").value = " ";'
html_txt  += '\n    document.getElementById("fp_ps_").value = " ";'
html_txt  += '\n    document.getElementById("gs_en_").value = "False";'
html_txt  += '\n    document.getElementById("gs_ap_").value = " ";'
html_txt  += '\n    document.getElementById("wi_en_").value = "False";'
html_txt  += '\n    document.getElementById("wi_nm_").value = " ";'
html_txt  += '\n    document.getElementById("wi_ps_").value = " ";'
html_txt  += '\n    document.getElementById("co_nm_").value = "Ista Sanat";'
html_txt  += '\n    document.getElementById("si_us_").value = "admin";'
html_txt  += '\n    document.getElementById("si_ps_").value = "admin";'
html_txt  += '\n    sm_tb_.style.display = \'none\';'
html_txt  += '\n    db_tb_.style.display = \'none\';'
html_txt  += '\n    ws_tb_.style.display = \'none\';'
html_txt  += '\n    gs_tb_.style.display = \'none\';'
html_txt  += '\n    wi_tb_.style.display = \'none\';'
html_txt  += '\n }'
html_txt  += '\n else {'
html_txt  += '\n     null'
html_txt  += '\n }}'
html_txt  += '\n</script>'

html_txt  += '\n</body>'
html_txt  += '\n</form>'
html_txt  += '\n</html>'



### Error Page Script (when user and pass are NOT correct)

html_error  = '\n<head>'
html_error  += '\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
html_error  += '\n<title>'+co_nm+'</title>'
html_error  += '\n<meta name="keywords" content="" />'
html_error  += '\n<meta name="description" content="" />'
html_error  += '\n<link href="http://'+output+'/signin.css" rel="stylesheet" type="text/css" media="all" />'
html_error  += '\n<link href="http://'+output+'/fonts.css" rel="stylesheet" type="text/css" media="all" />'
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
html_error  += '\n			<li><a accesskey="1" title="">Login ERROR !!!</a></li>'
html_error  += '\n		</ul>'
html_error  += '\n	</div>'
html_error  += '\n	<div id="three-column" class="container">'
html_error  += '\n		<div><span class="arrow-down"></span></div>'
html_error  += '\n		<div id="tbox1"><span class="icon icon-exclamation-sign"></span>'
html_error  += '\n		    </div>'
html_error  += '\n		<div id="tbox2">'
html_error  += '\n			<div class="title">'
html_error  += '\n			<h3>Incorrect Username or password.</h3></div>'
html_error  += '\n			<input type=button value="Back to Login Page" onclick=\'window.location.href="http://'+output+'"\' class="button">'
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
			print(html_txt)
		else:
			raise IOERROR
	else:
		raise IOERROR

except:
	#show results in HTML page
	print('Content-type: text/html\n')
	print(html_error)
