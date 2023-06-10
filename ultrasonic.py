"""
Module name: Ultrasonic sensor (HC-SR04) controller
Author: iCAROS7
Date: 10, June 2023
"""
import time

ECHO = [9, 25, 11, 8]   # Phys 21, 22, 23, 24 / 25 is GND
TRIG = [7, 0, 1, 5]     # Phys 26, 27, 28, 29

global GPIO


def init(_gpio):
    GPIO = _gpio

    print('INFO: Setup ultrasonic sensor')
    for echo in ECHO:
        GPIO.setup(echo, GPIO.IN)
        print(f'INFO: Setup ECHO mode at {echo}')
    for trig in TRIG:
        GPIO.setup(trig, GPIO.OUT)
        print(f'INFO: Setup TRIG mode at {trig}')
        GPIO.output(trig, False)
        print(f'INFO: Initialization at {trig}')

    print('INFO: Setup ultrasonic sensor done')


def get_dis():
    start, stop = 0, 0
    dis_arr = []

    for trig, echo, i in TRIG, ECHO, range(4):
        GPIO.output(trig, True)
        time.sleep(0.00001)
        GPIO.output(trig, False)

        while GPIO.input(echo) == 0:
            start = time.time()
        while GPIO.input(echo) == 1:
            stop = time.time()

        total_time = stop - start
        dis = total_time * 34300 / 2
        print(f'INFO: Get distance at {i} is %.1f' % dis)

        dis_arr.append(dis)

    return dis_arr
