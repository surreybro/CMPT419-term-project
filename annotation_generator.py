# -*- coding: utf-8 -*-
"""
To annotate images for the dataset
Created on Wed Jul 22 19:17:10 2020

@author:Justin
"""

# Imports

import os
import csv
import cv2
import sys

# Begin script

dir_path = 'dataset-master/'
images_subset = os.listdir(dir_path)
images_subset.sort(key=lambda x: int(x[:-4]))
image_paths = [os.path.join(dir_path, image_path) for image_path
               in images_subset]

# Create annotations.csv if it does not exist in current directory
if 'annotations.csv' not in os.listdir():
    prev_image_id = -1
    with open("annotations.csv", 'w', newline='') as new_csv:
        annotator_initial = input("Enter first letter of last name ")
        header = ['img_num',
                  'state'+annotator_initial,
                  'intensity'+annotator_initial,
                  'confidence'+annotator_initial]
        writer = csv.writer(new_csv)
        writer.writerow(header)

elif 'annotations.csv' in os.listdir():
    while True:
        try:
            prev_image_id = int(input("Enter the image id of the last image "
                                      "in the annotation.csv file -> "))
        except ValueError:
            print('not a number you dumbass, try again')
            continue
        else:
            break

states = {'a': 'happy', 'l': 'embarrassed', 'g': 'bad'}

for count, image_path in enumerate(image_paths):
    if count <= prev_image_id:
        continue

    image = cv2.imread(image_path)

    # waitKey returns ASCII Dec values, not keys themselves, so we use chr to
    # change the key press into something meaningful.
    cv2.imshow("Current_image", image)

    print('Annotate: a = Happy, l = Embarrassed, g = bad image, y = Quit')
    while True:
        try:
            state = chr(cv2.waitKey(0))
        except ValueError:
            print("you entered %s, this is not valid" % state)
            continue
        if state == 'y':
            cv2.destroyAllWindows()
            sys.exit()
        elif state != 'a' and state != 'l' and state != 'g':
            print("you entered %s, this is not valid" % state)
            print('Annotate: a = Happy, l = Embarrassed ')
            continue
        else:
            # success
            break

    state = states[state]

    if state == 'bad':
        print('bad image')
        res = [count, state, 'NA', 'NA']
        with open(r'annotations.csv', 'a', newline='') as fd:
            writer = csv.writer(fd)
            writer.writerow(res)
        continue

    print('Choose emotion intensity between 1:7')
    while True:
        try:
            intensity = int(cv2.waitKey(0)-ord('0'))
            
        except ValueError:
            print("you entered %s, this is not valid" % intensity)
            continue
        if intensity < 1 or intensity > 7:
            print("you entered %s, this is not valid" % intensity)
            print('Choose emotion intensity between 1:7')
            continue
        else:
            break

    print('Choose your annotation confidence between 1:7')
    while True:
        try:
            confidence = int(cv2.waitKey(0)-ord('0'))
            
        except ValueError:
            print("you entered %s, this is not valid" % confidence)
            continue
        if confidence < 1 or confidence > 7:
            print("you entered %s, this is not valid" % confidence)
            print('Choose emotion intensity between 1:7')
            continue
        else:
            break

    cv2.destroyAllWindows()

    res = [count, state, intensity, confidence]

    with open(r'annotations.csv', 'a', newline='') as fd:
        writer = csv.writer(fd)
        writer.writerow(res)
