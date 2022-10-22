# -*- coding: utf-8 -*-

#####################################################
#    Project:     Fire & Smoke Detection            #
#    Designer:    Hossein AalamShahi                #
#    Programmer:  Sina Shiri                        #
#    Date:        2019 Jul 30                       #
#    For:         Ista Sanat Co.                    #
#    File:        2ndStep of Detection              #
#    Des.:        some codes copied from Google API #
#####################################################

# Import needed modules
import os
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import tensorflow as tf
import argparse
import sys
import time
import datetime
from os.path import exists
import RPi.GPIO as GPIO

nnToggle = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(nnToggle, GPIO.OUT)
GPIO.output(nnToggle, False)

filePathFire = "/home/pi/IS/webserver/DB/frameCacheFire"
filePathSmoke = "/home/pi/IS/webserver/DB/frameCacheSmoke"
filePathDB = "/home/pi/IS/webserver/IMG_DB/"

# This is needed since the working directory is the object_detection folder.
sys.path.append('/home/pi/tensorflow1/models/research/object_detection')

# Import utilites
from utils import label_map_util
from utils import visualization_utils as vis_util

# Name of the directory containing the object detection module we're using
MODEL_NAME = 'inference_graph_RCNN_V3'

# Grab path to current working directory
CWD_PATH = '/home/pi/tensorflow1/models/research/object_detection'

# Path to frozen detection graph .pb file, which contains the model that is used
# for object detection.
PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

# Path to label map file
PATH_TO_LABELS = os.path.join(CWD_PATH,'data','smoke_labelmap.pbtxt')

# Number of classes the object detector can identify
NUM_CLASSES = 1

### Load the label map ###
# Label maps map indices to category names, so that when the convolution
# network predicts `5`, we know that this corresponds to `airplane`.
# Here we use internal utility functions, but anything that returns a
# dictionary mapping integers to appropriate string labels would be fine

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# Load the Tensorflow model into memory.
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.Session(graph=detection_graph)


# Define input and output tensors (i.e. data) for the object detection classifier

# Input tensor is the image
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

# Output tensors are the detection boxes, scores, and classes
# Each box represents a part of the image where a particular object was detected
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

# Each score represents level of confidence for each of the objects.
# The score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

# Number of objects detected
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

# Initialize calculation time for each
freq = cv2.getTickFrequency()

font = cv2.FONT_HERSHEY_SIMPLEX

fireFileCNT = 0
smokeFileCNT = 1
while(True):
    fireFileCNT += 1
    if (fireFileCNT == 10):
        fireFileCNT = 1
    firefilePath = filePathFire + str(fireFileCNT) + ".jpg"
    if (exists(firefilePath)):
        print("Detection Started")
        GPIO.output(nnToggle, True)
        try:
            t1 = cv2.getTickCount()

            # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
            # i.e. a single-column array, where each item in the column has the pixel RGB value
            frame = cv2.imread(firefilePath)
            
            os.remove(firefilePath)
            
            frame_expanded = np.expand_dims(frame, axis=0)

            # Perform the actual detection by running the model with the image as input
            (boxes, scores, classes, num) = sess.run(
                [detection_boxes, detection_scores, detection_classes, num_detections],
                feed_dict={image_tensor: frame_expanded})

            objects = []
            for index, value in enumerate(classes[0]):
              object_dict = {}
              if scores[0, index] > 0.5:
                object_dict[(category_index.get(value)).get('name').encode('utf8')] = \
                                    scores[0, index]
                objects.append(object_dict)
            
            # If Code Detect Something in Frame
            if (len(objects) > 0):
                fireDetect = False
                for l in range(0,len(objects)):
                    sm = list(objects[l])
                    print(sm)
                    if((sm[0] == b'fire') and (float(objects[l][sm[0]]) > 0.80)):
                        fireDetect = True
                # Draw the results of the detection
                
                if (fireDetect == True):
                    vis_util.visualize_boxes_and_labels_on_image_array(
                        frame,
                        np.squeeze(boxes),
                        np.squeeze(classes).astype(np.int32),
                        np.squeeze(scores),
                        category_index,
                        use_normalized_coordinates=True,
                        line_thickness=5)
                        #min_score_thresh=1)
                    
                    t2 = cv2.getTickCount()
                    time1 = (t2-t1)/freq
                    print("Duration: " + str(round(time1)))
                    
                    cv2.putText(frame,str(round(time1)),(30,50),font,1,(255,255,0),2,cv2.LINE_AA)
                    
                    fileName = str(datetime.datetime.now())[:19].replace(" ", "_")
                    fileName = fileName.replace("-", "").replace(":","") + ".jpg"
                    cv2.imwrite(filePathDB+fileName, frame)
                    
                    cmd = "python3 /home/pi/IS/alarm.py " + "-event=fire " + "-filename="+fileName + " &"
                    
                    #os.system(cmd)
                    
                    GPIO.output(nnToggle, False)
                
        except:
            print("ERROR")
            os.system("sudo reboot")
            
    smokefilePath = filePathSmoke + str(smokeFileCNT) + ".jpg"
    if (exists(smokefilePath)):
        print("Detection Started")
        GPIO.output(nnToggle, True)
        try:
            t1 = cv2.getTickCount()

            # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
            # i.e. a single-column array, where each item in the column has the pixel RGB value
            frame = cv2.imread(smokefilePath)
            
            os.remove(smokefilePath)
            
            frame_expanded = np.expand_dims(frame, axis=0)

            # Perform the actual detection by running the model with the image as input
            (boxes, scores, classes, num) = sess.run(
                [detection_boxes, detection_scores, detection_classes, num_detections],
                feed_dict={image_tensor: frame_expanded})
            
            objects = []
            for index, value in enumerate(classes[0]):
              object_dict = {}
              if scores[0, index] > 0.5:
                object_dict[(category_index.get(value)).get('name').encode('utf8')] = \
                                    scores[0, index]
                objects.append(object_dict)
            # If Code Detect Something in Frame
            if (len(objects) > 0):
                smokeDetect = False
                for l in range(0,len(objects)):
                    sm = list(objects[l])
                    if((sm[0] == b'w_smoke') and (float(objects[l][sm[0]]) > 0.98)):
                        smokeDetect = True
                # Draw the results of the detection
                if (smokeDetect == True):
                    vis_util.visualize_boxes_and_labels_on_image_array(
                        frame,
                        np.squeeze(boxes),
                        np.squeeze(classes).astype(np.int32),
                        np.squeeze(scores),
                        category_index,
                        use_normalized_coordinates=True,
                        line_thickness=5,
                        min_score_thresh=0.98)
                    
                    t2 = cv2.getTickCount()
                    time1 = (t2-t1)/freq
                    print("Duration: " + str(round(time1)))
                    
                    cv2.putText(frame,str(round(time1)),(30,50),font,1,(255,255,0),2,cv2.LINE_AA)
                    
                    fileName = str(datetime.datetime.now())[:19].replace(" ", "_")
                    fileName = fileName.replace("-", "").replace(":","") + ".jpg"
                    cv2.imwrite(filePathDB+fileName, frame)
                    
                    cmd = "python3 /home/pi/IS/alarm.py " + "-event=smoke " + "-filename="+fileName + " &"
                    
                    os.system(cmd)

                    GPIO.output(nnToggle, False)
                
        except:
            print("ERROR")
            os.system("sudo reboot")
    time.sleep(1)

cv2.destroyAllWindows()

