"""
Prjoect name: Smart Mower
Author: 이호민 (201735030), 조준영 (201735033)
Date: 10, June 2023
"""
import time

import RPi.GPIO as GPIO
import cv2
import numpy as np

import dcmotor
import ultrasonic
import buzzer

global camera
global net
global classes

conf_threshold = 0.5
nms_threshold = 0.4


def close():
    camera.release()
    cv2.destroyAllWindows()


def init():
    print('INFO: Setup camera')
    camera = cv2.VideoCapture(0)
    camera.set(3, 640)
    camera.set(4, 480)

    try:
        net = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')
        with open('coco.names', 'r') as f:
            classes = [line.strip() for line in f.readlines()]

    except IOError as e:
        print(f'ERROR: Not found "yolov3.cfg", "yolov3.weights" and "coco.names"\nLog: {e}')


GPIO.setmode(GPIO.BCM)

ultrasonic.init(GPIO)
dcmotor.init(GPIO)
buzzer.init(GPIO)
init()

while True:
    dis_arr = ultrasonic.get_dis()

    if dis_arr[0] > 5.0 and dis_arr[1] > 5.0 and dis_arr[2] > 5.0:  # 근방 5cm 이내 장애물 미 탐지시 전진
        dcmotor.forward(100)
    else:   # 근방 5cm 이내 장애물 탐지 시 카메라 인식 수행
        pass

    ret, frame = camera.read()
    blob = cv2.dnn.blobFromImage(frame, 1 / 255, (416, 416), swapRB=True, crop=False)

    net.setInput(blob)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > conf_threshold and (class_id == 0 or class_id == 56):
                center_x = int(detection[0] * frame.shape[1])
                center_y = int(detection[1] * frame.shape[0])
                width = int(detection[2] * frame.shape[1])
                height = int(detection[3] * frame.shape[0])

                x = int(center_x - width / 2)
                y = int(center_y - height / 2)

                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, width, height])

    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    for i in indices:
        i = i[0]
        box = boxes[i]
        x, y, width, height = box[0], box[1], box[2], box[3]

        cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 255, 0), 2)
        label = f'{classes[class_ids[i]]}: {confidences[i]:.2f}'
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        if classes[class_ids[i]] == 'person':
            dcmotor.stop()
            buzzer.beep()

            if dis_arr[3] > 10.0:
                dcmotor.reserve(50)
                time.sleep(3)
                dcmotor.stop()
                pass

        elif classes[class_ids[i]] == 'weed':
            dcmotor.forward(50)
            dcmotor.mow_on()
        else:
            dcmotor.mow_off()

    cv2.imshow('Camera', frame)

    if cv2.waitKey(1) == ord('q'):
        break

close()
