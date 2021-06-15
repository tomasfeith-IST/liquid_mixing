# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 09:33:46 2021

@author: tsfei
"""
import cv2
from PIL import Image
import time

def sigmoid_modified(x1,x2):
    if abs(x1-x2) < 20:
        return 1
    if abs(x1-x2) > 30:
        return 0
    return -abs(x1-x2)/10 + 3

def compare_pixels(pixel1, pixel2):
    return sigmoid_modified(pixel1[0],pixel2[0])*sigmoid_modified(pixel1[1],pixel2[1])*sigmoid_modified(pixel1[2],pixel2[2])

start_time = time.time()

videos = [
    '0.15ml.min_20rpm_cropped.mp4',
    '0.15ml.min_50rpm_cropped.mp4',
    '0.15ml.min_100rpm_cropped.mp4',
    '0.25ml.min_20rpm_cropped.mp4',
    '0.25ml.min_50rpm_cropped.mp4',
    '0.25ml.min_100rpm_cropped.mp4'
    ]

color = [
    [[127,183,142],[111,116,39]], #7fb78e + #6f7427
    [[0,140,136],[0,55,25]], #008c88 + #00370f
    [[0,118,118],[1,73,32]], #007676 + #014920
    [[0,117,126],[0,43,25]], #00757e + #002b15
    [[0,127,127],[0,64,46]], #007f7f + #00402e
    [[0,58,60],[0,38,25]] #003a3c + #002619
    ]

diff = [[],[],[],[],[],[]]
times = [[],[],[],[],[],[]]

for j in range(len(videos)):
    print('VIDEO', videos[j])
    vidcap = cv2.VideoCapture(videos[j])
    success,image = vidcap.read()
    count = 0
    part = 0
    # 5 points average
    while success:
        if (count % 2) == 0:
            if part == 4:
                diff[j][len(diff[j]) - 1] /= 4
                part = 0
            if part == 0:
                diff[j].append(0)
                times[j].append((count + 4)/30)
            # extract images from video
            print('Read a new Frame: ', success, count, ' frames read')
            image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            im = Image.fromarray(image)
            pixels = list(im.getdata())
            for i in range(len(pixels)):
                diff[j][len(diff[j]) - 1] += compare_pixels(pixels[i],color[j][0]) + compare_pixels(pixels[i],color[j][1])
            part += 1
        count += 1
        success,image = vidcap.read()

output = open('data.txt', 'w')
for j in range(len(videos)):
    print('VIDEO', videos[j], file=output)
    for k in range(len(diff[j])):
        print('Time', times[j][k], 'Value', diff[j][k], file=output)
output.close()

print("--- %s seconds ---" % (time.time() - start_time))
