# -*- coding: utf-8 -*-

#####################################################
#    Project:     Fire & Smoke Detection            #
#    Designer:    Hossein AalamShahi                #
#    Programmer:  Sina Shiri                        #
#    Date:        2019 Jul 13                       #
#    For:         Ista Sanat Co.                    #
#    File:        Creating Encrypted Files          #
#####################################################

# Modules
from cryptography.fernet import Fernet

### Create Encrypted file ###
# Read Decryption Key
file_ = open('key.key', 'rb')
key = file_.read()
f = Fernet(key)
file_.close()
# Get file name and path and Open FILE
data = ""
try:
	path = input("Import File Path : ")
	name = input("Import File Name : ")
	file_ = open(path + "/" + name, 'rb')
	data = file_.read().decode()
	file_.close()
except:
	print("\nPlease import address and name of file correctly.\n")
	
# Encrypting Data
encrypted = f.encrypt(data.encode())

# Save encrypted data into file 
file_ = open(path + "/" + name[:-4], 'wb')
file_.write(encrypted)
file_.close()
