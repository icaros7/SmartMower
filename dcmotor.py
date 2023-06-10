"""
Module name: DC Motor driver (L298n) controller
Author: iCAROS7
Date: 10, June 2023
"""

# Driver0: Vehicle control (Right, Left)
# Driver1: Mow control (Only one way)
ENABLE0 = [6, 12]           # Phys 31, 32
ENABLE1 = [13]              # Phys 33
INPUT0 = [19, 16, 26, 20]   # Phys 35, 36, 37, 38
INPUT1 = [10, 21]           # Phys 19, 40

global GPIO


def init(_gpio):
    GPIO = _gpio

    print('INFO: Setup DC motor driver')
    GPIO.setup(ENABLE0[0], GPIO.OUT)
    GPIO.setup(ENABLE0[1], GPIO.OUT)
    GPIO.setup(ENABLE1[0], GPIO.OUT)

    for gpio in INPUT0:
        GPIO.setup(gpio, GPIO.OUT)
    for gpio in INPUT1:
        GPIO.setup(gpio, GPIO.OUT)

    GPIO.output(INPUT1[0], True)
    GPIO.output(INPUT1[1], False)
    GPIO.output(ENABLE1[0], False)
    print('INFO: Setup DC motor driver done')


def forward():
    print('INFO: Set dc motor to Forward')
    GPIO.output(INPUT0[0], True)
    GPIO.output(INPUT0[1], False)
    GPIO.output(INPUT0[2], True)
    GPIO.output(INPUT0[3], False)

    GPIO.output(ENABLE0[0], True)
    GPIO.output(ENABLE0[1], True)


def reserve():
    print('INFO: Set dc motor to Reserve')
    GPIO.output(INPUT0[0], False)
    GPIO.output(INPUT0[1], True)
    GPIO.output(INPUT0[2], False)
    GPIO.output(INPUT0[3], True)

    GPIO.output(ENABLE0[0], True)
    GPIO.output(ENABLE0[1], True)


def stop():
    print('INFO: Set dc motor to Stop')
    GPIO.output(INPUT0[0], True)
    GPIO.output(INPUT0[1], True)
    GPIO.output(INPUT0[2], True)
    GPIO.output(INPUT0[3], True)

    GPIO.output(ENABLE0[0], True)
    GPIO.output(ENABLE0[1], True)


def right():
    print('INFO: Set dc motor to Right')
    GPIO.output(INPUT0[0], False)
    GPIO.output(INPUT0[1], True)
    GPIO.output(INPUT0[2], True)
    GPIO.output(INPUT0[3], False)

    GPIO.output(ENABLE0[0], True)
    GPIO.output(ENABLE0[1], True)


def left():
    print('INFO: Set dc motor to Left')
    GPIO.output(INPUT0[0], True)
    GPIO.output(INPUT0[1], False)
    GPIO.output(INPUT0[2], False)
    GPIO.output(INPUT0[3], True)

    GPIO.output(ENABLE0[0], True)
    GPIO.output(ENABLE0[1], True)


def mow_on():
    print('INFO: Set mower to On')
    GPIO.output(ENABLE1[0], True)


def mow_off():
    print('INFO: Set mower to Off')
    GPIO.output(ENABLE1[0], False)
