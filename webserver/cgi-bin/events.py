#!/usr/bin/python
# -*- coding: utf-8 -*-

#####################################################
#    Project:     Fire & Smoke Detection            #
#    Designer:    Hossein AalamShahi                #
#    Programmer:  Sina Shiri                        #
#    Date:        2019 Jul 26                       #
#    For:         Ista Sanat Co.                    #
#    File:        ControlPanel (Events Page)        #
#####################################################

# Add Needed Modules
from cryptography.fernet import Fernet
import os
import subprocess
import time
import cgi
import sqlite3
from os.path import exists

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

dbPath = "/home/pi/IS/webserver/DB/events.db"


def prebuild():
    ### Main Page Script for Status (when user click on Status Button)
    html_txt  = '\n'
    html_txt  += '\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
    html_txt  += '\n<title>'+co_nm+'</title>'
    #html_txt  += '\n<meta http-equiv="refresh" content="30">'
    html_txt  += '\n<meta charset="utf-8">'
    html_txt  += '\n<meta http-equiv="X-UA-Compatible" content="IE=edge">'
    html_txt  += '\n<meta name="viewport" content="width=device-width, initial-scale=1">'
    #html_txt  += '\n<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto|Varela+Round">'
    #html_txt  += '\n<link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">'
    html_txt  += '\n<link rel="stylesheet" href="http://'+ipaddr+'/events/font-awesome.min.css">'
    html_txt  += '\n<link rel="stylesheet" href="http://'+ipaddr+'/events/bootstrap.min.css">'
    html_txt  += '\n<link href="http://'+ipaddr+'/events.css" rel="stylesheet" type="text/css" media="all" />'
    html_txt  += '\n<link href="http://'+ipaddr+'/fonts.css" rel="stylesheet" type="text/css" media="all" />'
    html_txt  += '\n<script src="http://'+ipaddr+'/events/jquery.min.js"></script>'
    html_txt  += '\n<script src="http://'+ipaddr+'/events/bootstrap.min.js"></script>'
    html_txt  += '\n<style type="text/css">'
    html_txt  += '\n	.table-wrapper {'
    html_txt  += '\n        width: 1100px;'
    html_txt  += '\n        background: #fff;'
    html_txt  += '\n        padding: 20px 30px 5px;'
    html_txt  += '\n        margin: 30px auto;'
    html_txt  += '\n        box-shadow: 0 0 1px 0 rgba(0,0,0,.25);'
    html_txt  += '\n    }'
    html_txt  += '\n	.table-title .btn-group {'
    html_txt  += '\n		float: right;'
    html_txt  += '\n	}'
    html_txt  += '\n	.table-title .btn {'
    html_txt  += '\n		min-width: 50px;'
    html_txt  += '\n		border-radius: 2px;'
    html_txt  += '\n		border: none;'
    html_txt  += '\n		padding: 6px 12px;'
    html_txt  += '\n		font-size: 95%;'
    html_txt  += '\n		outline: none !important;'
    html_txt  += '\n		height: 30px;'
    html_txt  += '\n	}'
    html_txt  += '\n    .table-title {'
    html_txt  += '\n		border-bottom: 1px solid #e9e9e9;'
    html_txt  += '\n		padding-bottom: 15px;'
    html_txt  += '\n		margin-bottom: 5px;'
    html_txt  += '\n		background: rgb(0, 50, 74);'
    html_txt  += '\n		margin: -20px -31px 10px;'
    html_txt  += '\n		padding: 15px 30px;'
    html_txt  += '\n		color: #fff;'
    html_txt  += '\n    }'
    html_txt  += '\n    .table-title h2 {'
    html_txt  += '\n		margin: 2px 0 0;'
    html_txt  += '\n		font-size: 24px;'
    html_txt  += '\n	}'
    html_txt  += '\n    table.table tr th, table.table tr td {'
    html_txt  += '\n        border-color: #e9e9e9;'
    html_txt  += '\n		padding: 12px 15px;'
    html_txt  += '\n		vertical-align: middle;'
    html_txt  += '\n    }'
    html_txt  += '\n	table.table tr th:first-child {'
    html_txt  += '\n		width: 40px;'
    html_txt  += '\n	}'
    html_txt  += '\n	table.table tr th:last-child {'
    html_txt  += '\n		width: 100px;'
    html_txt  += '\n	}'
    html_txt  += '\n    table.table-striped tbody tr:nth-of-type(odd) {'
    html_txt  += '\n    	background-color: #fcfcfc;'
    html_txt  += '\n	}'
    html_txt  += '\n	table.table-striped.table-hover tbody tr:hover {'
    html_txt  += '\n		background: #f5f5f5;'
    html_txt  += '\n	}'
    html_txt  += '\n    table.table td a {'
    html_txt  += '\n        color: #2196f3;'
    html_txt  += '\n    }'
    html_txt  += '\n	table.table td .btn.manage {'
    html_txt  += '\n		padding: 2px 10px;'
    html_txt  += '\n		background: #37BC9B;'
    html_txt  += '\n		color: #fff;'
    html_txt  += '\n		border-radius: 2px;'
    html_txt  += '\n	}'
    html_txt  += '\n	table.table td .btn.manage:hover {'
    html_txt  += '\n		background: #2e9c81;		'
    html_txt  += '\n	}'
    html_txt  += '\n</style>'
    html_txt  += '\n<script type="text/javascript">'
    html_txt  += '\n$(document).ready(function(){'
    html_txt  += '\n	$(".btn-group .btn").click(function(){'
    html_txt  += '\n		var inputValue = $(this).find("input").val();'
    html_txt  += '\n		if(inputValue != \'all\'){'
    html_txt  += '\n			var target = $(\'table tr[data-status="\' + inputValue + \'"]\');'
    html_txt  += '\n			$("table tbody tr").not(target).hide();'
    html_txt  += '\n			target.fadeIn();'
    html_txt  += '\n		} else {'
    html_txt  += '\n			$("table tbody tr").fadeIn();'
    html_txt  += '\n		}'
    html_txt  += '\n	});'
    html_txt  += '\n	// Changing the class of status label to support Bootstrap 4'
    html_txt  += '\n    var bs = $.fn.tooltip.Constructor.VERSION;'
    html_txt  += '\n    var str = bs.split(".");'
    html_txt  += '\n    if(str[0] == 4){'
    html_txt  += '\n        $(".label").each(function(){'
    html_txt  += '\n        	var classStr = $(this).attr("class");'
    html_txt  += '\n            var newClassStr = classStr.replace(/label/g, "badge");'
    html_txt  += '\n            $(this).removeAttr("class").addClass(newClassStr);'
    html_txt  += '\n        });'
    html_txt  += '\n    }'
    html_txt  += '\n});'
    html_txt  += '\n</script>'
    html_txt  += '\n</head>'
    html_txt  += '\n<body>'
    html_txt  += '\n<form>'
    html_txt  += '\n<div id="logo" class="container">'
    html_txt  += '\n	<h1><span class="icon icon-tag icon-size"></span><a>Fire & Smoke <span>Detector</span></a></h1>'
    html_txt  += '\n	<p>'+co_nm+'</a></p></div>'
    html_txt  += '\n	<div class="container"><div class="buttonjustify">'
    html_txt  += '\n	<input type="button" value="Delete Events"  class="button">' #onClick="delDB()"
    html_txt  += '\n <input type=button value="Back" onclick=\'goBack();\' class="button"></div></div><br><br>'
    html_txt  += '\n <script>'
    html_txt  += '\n function goBack() {'
    html_txt  += '\n   window.history.back()'
    html_txt  += '\n }'
    html_txt  += '\n </script>'
    html_txt  += '\n <script>'
    html_txt  += '\n function delDB() {'
    html_txt  += '\n    var request = new XMLHttpRequest();'
    html_txt  += '\n    request.open("GET", "http://'+ipaddr+'/cgi-bin/delDB.py", true);'
    html_txt  += '\n    request.send();'
    html_txt  += '\n }'
    html_txt  += '\n </script>'
    html_txt  += '\n<div id="wrapper" class="container">'
    html_txt  += '\n	<div id="menu" class="container">'
    html_txt  += '\n		<ul>'
    html_txt  += '\n			<li class="current_page_item"></li>'
    html_txt  += '\n			<li><a accesskey="1" title="">Manage Events</a></li>'
    html_txt  += '\n		</ul>'
    html_txt  += '\n	</div>'
    html_txt  += '\n	<div id="three-column" class="container">'
    html_txt  += '\n    <div class="table-wrapper">'
    html_txt  += '\n        <div class="table-title">'
    html_txt  += '\n            <div class="row">'
    html_txt  += '\n                <div class="col-sm-6"></div>'
    html_txt  += '\n                <div class="col-sm-6">'
    html_txt  += '\n                    <div class="btn-group" data-toggle="buttons">'
    html_txt  += '\n                        <label class="btn btn-info active">'
    html_txt  += '\n                            <input type="radio" name="status" value="all" checked="checked"> All'
    html_txt  += '\n                        </label>'
    html_txt  += '\n                        <label class="btn btn-success">'
    html_txt  += '\n                            <input type="radio" name="status" value="smoke"> SMOKE'
    html_txt  += '\n                        </label>'
    html_txt  += '\n                        <label class="btn btn btn-danger">'
    html_txt  += '\n                            <input type="radio" name="status" value="fire"> FIRE'
    html_txt  += '\n                        </label>'
    html_txt  += '\n                        <label class="btn btn btn-warning">'
    html_txt  += '\n                            <input type="radio" name="status" value="prealarm"> PRE-ALARM'
    html_txt  += '\n                        </label>'
    html_txt  += '\n                    </div>'
    html_txt  += '\n                </div>'
    html_txt  += '\n            </div>'
    html_txt  += '\n        </div>'
    html_txt  += '\n        <table id="tb" class="table table-striped table-hover">'
    html_txt  += '\n            <thead>'
    html_txt  += '\n                <tr>'
    html_txt  += '\n                    <th style="text-align:center">#</th>'
    html_txt  += '\n                    <th style="text-align:center">Event</th>'
    html_txt  += '\n                    <th style="text-align:center">Date</th>'
    html_txt  += '\n                    <th style="text-align:center">Time</th>'
    html_txt  += '\n                    <th style="text-align:center">ScreenShot</th>'
    html_txt  += '\n                    <th style="text-align:center">Emerg.</th>'
    html_txt  += '\n                    <th style="text-align:center">Local&nbsp;DB</th>'
    html_txt  += '\n                    <th style="text-align:center">Web&nbsp;Server</th>'
    html_txt  += '\n                    <th style="text-align:center">Method</th>'
    html_txt  += '\n                    <th style="text-align:center">SMS</th>'
    html_txt  += '\n                </tr>'
    html_txt  += '\n            </thead>'
    html_txt  += '\n            <tbody>'
    
    if (exists(dbPath)):
        # Get Data from SQLite
        addrss = sqlite3.connect(dbPath)
        cb = addrss.cursor()
        cb.execute('SELECT * FROM {tn} ORDER BY DTSR DESC'.\
                        format(tn="events"))
        allData = cb.fetchall()
        addrss.close()
        
        for i in range(0,len(allData)):
            html_txt  += '\n                <tr data-status="'+allData[i][3]+'">'
            html_txt  += '\n                <td align=\"center\">'+str(i+1)+'</td>'
            if (allData[i][3]=="fire"):
                html_txt  += '\n                <td align=\"center\"><span class=\"label label-danger\">FIRE</span></td>'
            elif (allData[i][3]=="smoke"):
                html_txt  += '\n                <td align=\"center\"><span class=\"label label-success\">SMOKE</span></td>'
            else:
                html_txt  += '\n                <td align=\"center\"><span class=\"label label-warning\">PRE-ALARM</span></td>'
            html_txt  += '\n                <td align=\"center\">'+allData[i][4]+'</td>'
            html_txt  += '\n                <td align=\"center\">'+allData[i][5]+'</td>'
            html_txt  += '\n                <td align=\"center\"><a href=\"http://'+ipaddr+'/IMG_DB/'+allData[i][7]+'\" target=\"_blank\" class=\"btn btn-sm manage\">View</a></td>'
            html_txt  += '\n                <td align=\"center\">'+allData[i][8]+'</td>'
            html_txt  += '\n                <td align=\"center\">'+allData[i][9]+'</td>'
            html_txt  += '\n                <td align=\"center\">'+allData[i][10]+'</td>'
            html_txt  += '\n                <td align=\"center\">'+allData[i][11]+'</td>'
            html_txt  += '\n                <td align=\"center\">'+allData[i][12]+'</td>'
            html_txt  += '\n                </tr>'
    html_txt  += '\n            </tbody>'
    html_txt  += '\n        </table>'
    html_txt  += '\n    </div>'
    html_txt  += '\n	</div></div></div></div>'
    html_txt  += '\n<script type="text/javascript" src="http://'+ipaddr+'/events/export/jquery-3.2.1.min.js"></script>'
    html_txt  += '\n<script type="text/javascript" src="http://'+ipaddr+'/events/export/FileSaver.min.js"></script>'
    html_txt  += '\n<script type="text/javascript" src="http://'+ipaddr+'/events/export/xlsx.core.min.js"></script>'
    html_txt  += '\n<script type="text/javascript" src="http://'+ipaddr+'/events/export/es6-promise.auto.min.js"></script>'
    html_txt  += '\n<script type="text/javascript" src="http://'+ipaddr+'/events/export/html2canvas.min.js"></script>'
    html_txt  += '\n<script type="text/javascript" src="http://'+ipaddr+'/events/export/jspdf.min.js"></script>'
    html_txt  += '\n<script type="text/javascript" src="http://'+ipaddr+'/events/export/jspdf.plugin.autotable.js"></script>'
    html_txt  += '\n<script type="text/javascript" src="http://'+ipaddr+'/events/export/tableExport.js"></script>'
    html_txt  += '\n	<div id="menu" class="container">'
    html_txt  += '\n		<ul>'
    html_txt  += '\n			<li><a accesskey="1" title="">Export Data</a></li><br>'
    html_txt  += '\n			<input type=button onclick="$(\'#tb\').tableExport({type:\'pdf\',escape:\'false\'});" value="PDF" class="button"></li>'
    html_txt  += '\n			<input type=button onclick="$(\'#tb\').tableExport({type:\'excel\',escape:\'false\'});" value="EXCEL" class="button"></li>'
    html_txt  += '\n			<input type=button onclick="$(\'#tb\').tableExport({type:\'csv\',escape:\'false\'});" value="CSV" class="button"></li>'
    html_txt  += '\n			<input type=button onclick="$(\'#tb\').tableExport({type:\'json\',escape:\'false\'});" value="JSON" class="button"></li>'
    html_txt  += '\n		</ul><br><br>'
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
html_error  += '\n	<h1><span class="icon icon-tag icon-size"></span><a>Fire & Smoke <span>Detector</span></a></h1>'
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
html_error  += '\n	<p><a>&copy;All rights reserved. | Designed by IstaSanat +98-914-400-2264</a><br><a>Firmware version: '+fr_vr+'</a></p>'
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
