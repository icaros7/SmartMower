"""
Prjoect name: Smart Mower
Author: 이호민 (201735030), 조준영 (201735033)
Date: 10, June 2023
"""
import ultrasonic
import dcmotor

import RPi.GPIO as GPIO
import cv2
import numpy as np
import time

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

while True:
    # TODO: ultrasonic.get_dis()를 통해 읽어온 초음파 정보로 이동 판단 알고리즘 추가
    dis_arr = ultrasonic.get_dis()

    if dis_arr[0] < 5.0:  # TODO: 예시, 전방 5cm가 안남았으면 멈춰라
        dcmotor.stop()

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
            # TODO: 사람 회피 동작
            dcmotor.stop()  # TODO: 예시, 차량 정지

        if classes[class_ids[i]] == 'weed':
            # TODO: 잡초 탐지 동작
            dcmotor.left()  # TODO: 예시, 왼쪽으로 1초 몸을 튼 후 다시 전진
            time.sleep(1)
            dcmotor.forward()

    cv2.imshow('Camera', frame)

    if cv2.waitKey(1) == ord('q'):
        break
