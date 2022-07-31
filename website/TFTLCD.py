
import RPi.GPIO as GPIO
import time
import os

'''
하드웨어 핀 연결도
'''
dataPin = [13,6,5,11,9,10,22,27,17] # D0~D7
RS = 21
CS = 16
RD = 20
WR = 26
RES = 19
BLK = 12

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for i in range(8):
    GPIO.setup(dataPin[i], GPIO.OUT, initial=GPIO.HIGH)

