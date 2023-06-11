"""
Module name: Piezo Buzzer controller
Author: iCAROS7
Date: 11, June 2023
"""
import time

global GPIO
global PWM

BUZZ = 22   # Phys 15


def init(_gpio):
    GPIO = _gpio
    GPIO.setup(BUZZ, GPIO.OUT)
    PWM = GPIO.PWM(BUZZ, 262)   # 4 Octa C
    PWM.start(0)


def beep():
    PWM.ChangeDutyCycle(50)
    time.sleep(3)
    PWM.ChangeDutyCycle(0)
    time.sleep(1)
    PWM.ChangeDutyCycle(50)
    time.sleep(3)
    PWM.ChangeDutyCycle(0)
    time.sleep(1)
    PWM.ChangeDutyCycle(50)
    time.sleep(3)
    PWM.ChangeDutyCycle(0)


def clean():
    PWM.stop()
