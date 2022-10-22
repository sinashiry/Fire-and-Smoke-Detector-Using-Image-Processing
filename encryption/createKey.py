# -*- coding: utf-8 -*-

#####################################################
#    Project:     Fire & Smoke Detection            #
#    Designer:    Hossein AalamShahi                #
#    Programmer:  Sina Shiri                        #
#    Date:        2019 Jul 13                       #
#    For:         Ista Sanat Co.                    #
#    File:        Creating cryptography key         #
#####################################################

# Modules
from cryptography.fernet import Fernet





### Create Key file ###
key = Fernet.generate_key()
file = open('key.key', 'wb')
file.write(key) # The key is type bytes still
file.close()
