# -*- coding: utf-8 -*-

#####################################################
#    Project:     Fire & Smoke Detection            #
#    Designer:    Hossein AalamShahi                #
#    Programmer:  Sina Shiri                        #
#    Date:        2019 Jul 25                       #
#    For:         Ista Sanat Co.                    #
#    File:        WebServer Controller              #
#####################################################

import os, sys
import subprocess
from http.server import HTTPServer, CGIHTTPRequestHandler
import time

webdir = '.'
port   = 80

def getIP():
    try:
        while(True):
            output = subprocess.Popen(["hostname", "-I"],stdout = subprocess.PIPE).communicate()[0]
            if (len(output) > 6):
                buildServer()
            else:
                print("No IP")
                time.sleep(1)
    except:
        print("Error")
        getIP()

def buildServer():
    print("Started")
    os.chdir(webdir)
    srvraddr = ("", port)
    srvrobj  = HTTPServer(srvraddr, CGIHTTPRequestHandler)
    srvrobj.serve_forever()

#getIP()
buildServer()
