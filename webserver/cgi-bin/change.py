# -*- coding: utf-8 -*-

#####################################################
#    Project:     Fire & Smoke Detection            #
#    Designer:    Hossein AalamShahi                #
#    Programmer:  Sina Shiri                        #
#    Date:        2019 Jul 27                       #
#    For:         Ista Sanat Co.                    #
#    File:        ControlPanel (Set WiFi settings)  #
#####################################################


# Add Needed Modules
from cryptography.fernet import Fernet

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

if (wi_en == "True"):
    wifile_ = open("/etc/wpa_supplicant/wpa_supplicant.conf", 'w')

    wifi_txt  = "country=US\n"
    wifi_txt += "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n"
    wifi_txt += "update_config=1\n\n"
    wifi_txt += "network={\n"
    wifi_txt += " ssid=\"" + wi_nm + "\"\n"
    wifi_txt += " scan_ssid=1\n"
    wifi_txt += " psk=\"" + wi_ps + "\"\n"
    wifi_txt += " key_mgmt=WPA-PSK\n"
    wifi_txt += "}"

    wifile_.write(wifi_txt)
    wifile_.close()
else:
    None
