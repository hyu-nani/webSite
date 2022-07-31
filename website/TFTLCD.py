
import RPi.GPIO as GPIO
import time
import os

'''
하드웨어 핀 연결도 GPIO핀
'''
dataPin = [13,6,5,11,9,10,22,27,17] # D0~D7
RS = 21 #D/C
CS = 16
RD = 20
WR = 26
RES = 19
BLK = 12

def TFTgpio_set():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for i in range(8):
        GPIO.setup(dataPin[i], GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(RS, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(CS, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(RD, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(WR, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(RES, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(BLK, GPIO.OUT, initial=GPIO.HIGH)

def LCDdata(bit):
    for i in range(8):
        if bit & (1 << i) == 1:
            GPIO.output(dataPin[i],GPIO.HIGH)
        else:
            GPIO.output(dataPin[i],GPIO.LOW)

def LCD_init():
    GPIO.output(CS,GPIO.LOW)#active
    #setting
    GPIO.output(RS,GPIO.LOW)
    GPIO.output(RD,GPIO.HIGH)
    GPIO.output(WR,GPIO.LOW)
    LCDdata(0x01)#reset
    GPIO.output(WR,GPIO.HIGH)


TFTgpio_set()
LCD_init()