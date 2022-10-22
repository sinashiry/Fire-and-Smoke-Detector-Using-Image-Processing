#!/usr/bin/python
# -*- coding: utf-8 -*-

#####################################################
#    Project:     Fire & Smoke Detection            #
#    Designer:    Hossein AalamShahi                #
#    Programmer:  Sina Shiri                        #
#    Date:        2019 Jul 26                       #
#    For:         Ista Sanat Co.                    #
#    File:        ControlPanel (Reboot Page)        #
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
# Login INFO
si_us = form.getvalue('si_us')
si_ps = form.getvalue('si_ps')
#COMPANY NAME & FirmWare
co_nm = form.getvalue('co_nm')
fr_vr = form.getvalue('fr_vr')
#Zone info
zn_nm = form.getvalue('zn_nm')
zn_md = form.getvalue('zn_md')
#SMS info
sm_en = form.getvalue('sm_en')
pn_1 = form.getvalue('pn_1')
pn_1_ch = form.getvalue('pn_1_ch')
pn_2 = form.getvalue('pn_2')
pn_2_ch = form.getvalue('pn_2_ch')
pn_3 = form.getvalue('pn_3')
pn_3_ch = form.getvalue('pn_3_ch')
sm_pn = ""
if(pn_1 != None):
    if(len(pn_1) == 13):
        sm_pn = sm_pn + pn_1
        if(pn_1_ch == "on"):
            sm_pn = sm_pn + "*,"
        else:
            sm_pn = sm_pn + ","
    else:
        sm_pn = sm_pn + ","
else:
    sm_pn = sm_pn + ","
if(pn_2 != None):
    if(len(pn_2) == 13):
        sm_pn = sm_pn + pn_2
        if(pn_2_ch == "on"):
            sm_pn = sm_pn + "*,"
        else:
            sm_pn = sm_pn + ","
    else:
        sm_pn = sm_pn + ","
else:
    sm_pn = sm_pn + ","
if(pn_3 != None):
    if(len(pn_3) == 13):
        sm_pn = sm_pn + pn_3
        if(pn_3_ch == "on"):
            sm_pn = sm_pn + "*"
        else:
            sm_pn = sm_pn + ""
    else:
        sm_pn = sm_pn + ","
else:
    sm_pn = sm_pn + ","
#GSM info
gs_en = form.getvalue('gs_en')
gs_ap = form.getvalue('gs_ap')
# Local Server
db_en = form.getvalue('db_en')
dbip1 = form.getvalue('db_ip1')
dbip2 = form.getvalue('db_ip2')
dbip3 = form.getvalue('db_ip3')
dbip4 = form.getvalue('db_ip4')
db_ip = dbip1 + "." + dbip2 + "." + dbip3 + "." + dbip4
db_pt = form.getvalue('db_pt')
db_us = form.getvalue('db_us')
db_ps = form.getvalue('db_ps')
db_nm = form.getvalue('db_nm')
#WebServer info
ws_en = form.getvalue('ws_en')
ws_ad = form.getvalue('ws_ad')
ws_ul = form.getvalue('ws_ul')
#FTP info
fp_ad = form.getvalue('fp_ad')
fp_pt = form.getvalue('fp_pt')
fp_us = form.getvalue('fp_us')
fp_ps = form.getvalue('fp_ps')
# Alarm
pa_en = form.getvalue('pa_en')
al_en = form.getvalue('al_en')
# WiFi
wi_en = form.getvalue('wi_en')
wi_nm = form.getvalue('wi_nm')
wi_ps = form.getvalue('wi_ps')
#NEW PASSWORD CONFIRM
coms = form.getvalue('coms')
clgp = form.getvalue('clgp')
nlgp = form.getvalue('nlgp')
if(coms == "Matching"):
    si_ps = nlgp
else:
    None


#html format of saved mode page

html_txt  = '\n<head>'
html_txt  += '\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
html_txt  += '\n<title>'+co_nm+'</title>'
html_txt  += '\n<meta name="keywords" content="" />'
html_txt  += '\n<meta name="description" content="" />'
html_txt  += '\n<link href="http://'+output+'/signin.css" rel="stylesheet" type="text/css" media="all" />'
html_txt  += '\n<link href="http://'+output+'/fonts.css" rel="stylesheet" type="text/css" media="all" />'
html_txt  +='<script>'
html_txt  +='setTimeout(function gosign(){'
html_txt  +='	window.location.href="signin.py"'
html_txt  +='},4000);'	
html_txt  +='</script>'
html_txt  += '\n</head>'
html_txt  += '\n<body>'
html_txt  += '\n<form>'
html_txt  += '\n<div id="logo" class="container">'
html_txt  += '\n	<h1><span class="icon icon-tags icon-size"></span><a>Fire & Smoke <span>Detector</span></a></h1>'
html_txt  += '\n	<p>'+co_nm+'</a></p></div>'
html_txt  += '\n</div>'
html_txt  += '\n<div id="wrapper" class="container">'
html_txt  += '\n	<div id="menu" class="container">'
html_txt  += '\n		<ul>'
html_txt  += '\n			<li class="current_page_item"></li>'
html_txt  += '\n			<li><a accesskey="1" title="">System Rebooting !!!</a></li>'
html_txt  += '\n		</ul>'
html_txt  += '\n	</div>'
html_txt  += '\n	<div id="three-column" class="container">'
html_txt  += '\n		<div><span class="arrow-down"></span></div>'
html_txt  += '\n		<div id="tbox1"><span class="icon icon-ok-sign"></span>'
html_txt  += '\n		    </div>'
html_txt  += '\n		<div id="tbox2">'
html_txt  += '\n			<div class="title">'
html_txt  += '\n			<h3>Settings Changed Successfully</h3>'
html_txt  += '\n			<h3>System will Reboot after 5 Seconds.</h3></div>'
html_txt  += '\n        </div>'
html_txt  += '\n	</div>'
html_txt  += '\n</div>'
html_txt  += '\n<div id="copyright">'
html_txt  += '\n	<p><a>&copy;All rights reserved. | Designed by IstaSanat +98-914-400-2264</a><br><a>Firmware version: '+fr_vr+'</a></p>'
html_txt  += '\n</div>'
html_txt  += '\n</body>'
html_txt  += '\n</form>'
html_txt  += '\n</html>'

#html format of error mode page

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
html_error  += '\n	<h1><span class="icon icon-tags icon-size"></span><a>Fire & Smoke <span>Detector</span></a></h1>'
html_error  += '\n	<p>'+co_nm+'</a></p></div>'
html_error  += '\n</div>'
html_error  += '\n<div id="wrapper" class="container">'
html_error  += '\n	<div id="menu" class="container">'
html_error  += '\n		<ul>'
html_error  += '\n			<li class="current_page_item"></li>'
html_error  += '\n			<li><a accesskey="1" title="">SAVE ERROR !!!</a></li>'
html_error  += '\n		</ul>'
html_error  += '\n	</div>'
html_error  += '\n	<div id="three-column" class="container">'
html_error  += '\n		<div><span class="arrow-down"></span></div>'
html_error  += '\n		<div id="tbox1"><span class="icon icon-warning-sign"></span>'
html_error  += '\n		    </div>'
html_error  += '\n		<div id="tbox2">'
html_error  += '\n			<div class="title">'
html_error  += '\n			<h3>Wrong Format for Some fields.</h3>'
html_error  += '\n			<h3>Settings NOT Changed.</h3></div>'
html_error  += '\n			<input type=button value="Back to Login Page" onclick=\'window.location.href="http://'+output+'"\' class="button">'
html_error  += '\n        </div>'
html_error  += '\n	</div>'
html_error  += '\n</div>'
html_error  += '\n<div id="copyright">'
html_error  += '\n	<p><a>&copy;All rights reserved. | Designed by IstaSanat +98-914-400-2264</a><br><a>Firmware version: '+fr_vr+'</a></p>'
html_error  += '\n</div>'
html_error  += '\n</body>'
html_error  += '\n</form>'
html_error  += '\n</html>'

try:
    # Write Settings in txt file
    txt  = "####__SIGNIN__#####"
    txt += "\nsi-us=" + si_us
    txt += "\nsi-ps=" + si_ps
    txt += "\n###_COMPANY_NAME_##"
    txt += "\nco-nm=" + co_nm
    txt += "\nfr-vr=" + fr_vr
    txt += "\n#######_ZONE_######"
    txt += "\nzn-nm=" + zn_nm
    txt += "\nzn-md=" + zn_md
    txt += "\n#######_SMS_#######"
    txt += "\nsm-en=" + sm_en
    txt += "\nsm-pn=" + sm_pn
    txt += "\n#######_APN_#######"
    txt += "\ngs-en=" + gs_en
    txt += "\ngs-ap=" + gs_ap
    txt += "\n##_DATABASE_LOCAL_#"
    txt += "\ndb-en=" + db_en
    txt += "\ndb-ip=" + db_ip
    txt += "\ndb-pt=" + db_pt
    txt += "\ndb-us=" + db_us
    txt += "\ndb-ps=" + db_ps
    txt += "\ndb-nm=" + db_nm
    txt += "\n###_WEB_SERVER_###"
    txt += "\nws-en=" + ws_en
    txt += "\nws-ad=" + ws_ad
    txt += "\nws-ul=" + ws_ul
    txt += "\n###_FTP_SERVER_###"
    txt += "\nfp-ad=" + fp_ad
    txt += "\nfp-pt=" + fp_pt
    txt += "\nfp-us=" + fp_us
    txt += "\nfp-ps=" + fp_ps
    txt += "\n###ALARM_ENABLE###"
    txt += "\npa-en=" + pa_en
    txt += "\nal-en=" + al_en
    txt += "\n######_WiFi_######"
    txt += "\nwi-en=" + wi_en
    txt += "\nwi-nm=" + wi_nm
    txt += "\nwi-ps=" + wi_ps
    txt += "\n##################"
    # Read Decryption Key
    file = open('/home/pi/IS/encryption/key.key', 'rb')
    key = file.read()
    f = Fernet(key)
    file.close()
    # Save Settings in encrypted Format
    encrypted = f.encrypt(txt)
    with open('/home/pi/IS/settings/settings', 'wb') as fi:
        fi.write(encrypted)

    #Change WiFi settings
    os.system("(python3 /home/pi/IS/webserver/cgi-bin/change.py) &")

    # Show Results in HTML page    
    print('Content-type: text/html\n')
    print(html_txt)

    #reboot system
    os.system("(sleep 8; reboot) &")

except: 
    #show error results in HTML page
    print(html_error)

