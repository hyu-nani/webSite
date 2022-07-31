
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
        if (bit & (1 << i)) == 1:
            GPIO.output(dataPin[i],GPIO.HIGH)
            print("1")
        else:
            GPIO.output(dataPin[i],GPIO.LOW)
            print("0")
        print("\n")
        time.sleep(0.5)

def writeCammand(bit):
    GPIO.output(RS,GPIO.LOW)
    GPIO.output(RD,GPIO.HIGH)
    GPIO.output(WR,GPIO.LOW)
    LCDdata(bit)
    GPIO.output(WR,GPIO.HIGH)

def writeData(bit):
    GPIO.output(RS,GPIO.HIGH)
    GPIO.output(RD,GPIO.HIGH)
    GPIO.output(WR,GPIO.LOW)
    LCDdata(bit)
    GPIO.output(WR,GPIO.HIGH)

def LCD_init():
    GPIO.output(CS,GPIO.LOW)# active
    # start inittial code
    GPIO.output(RES,GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(RES,GPIO.LOW)
    time.sleep(0.01)
    GPIO.output(RES,GPIO.HIGH)
    time.sleep(0.12)
    writeCammand(0x01)# reset
    time.sleep(0.005)
    writeCammand(0x28)# display OFF
    
    writeCammand(0xC0)# power control 1
    writeData(0x26)
    writeCammand(0xC1)# power control 2
    writeData(0x11)
    writeCammand(0xC5)# vcom control 1
    writeData(0x5C)
    writeData(0x4C)
    writeCammand(0xC7)# vcom control 2
    writeData(0x94)

    writeCammand(0x36)# memory access control
    writeData(0x48)
    writeCammand(0x3A)# pixel format rate
    writeData(0x66) #[ DPI:110  / DBI:110 ] 262K color: 18-bit/pixel (RGB 6-6-6 bits input)

    writeCammand(0xB1)# frame rate
    writeData(0x00)
    writeData(0x1B)# 70(default)

    writeCammand(0x26)# Gamma Set
    writeData(0x01)

    writeCammand(0xE0)# Positive Gamma Correction
    writeData(0x1F)
    writeData(0x1A)
    writeData(0x18)
    writeData(0x0A)
    writeData(0x0F)
    writeData(0x06)
    writeData(0x45)
    writeData(0x87)
    writeData(0x32)
    writeData(0x0A)
    writeData(0x07)
    writeData(0x02)
    writeData(0x07)
    writeData(0x05)
    writeData(0x00)
    writeCammand(0xE1)# Negative Gamma Correction
    writeData(0x00)
    writeData(0x25)
    writeData(0x27)
    writeData(0x05)
    writeData(0x10)
    writeData(0x09)
    writeData(0x3A)
    writeData(0x78)
    writeData(0x4D)
    writeData(0x05)
    writeData(0x18)
    writeData(0x0D)
    writeData(0x38)
    writeData(0x3A)
    writeData(0x1F)

    writeCammand(0x2A)# column address set
    writeData(0x00)
    writeData(0x00)
    writeData(0x00)
    writeData(0xEF)
    writeCammand(0x2B)# page address set
    writeData(0x00)
    writeData(0x00)
    writeData(0x01)
    writeData(0x3F)
    writeCammand(0xB6)# Display Function Control
    writeData(0x0A)
    writeData(0x82)
    writeData(0x27)
    writeData(0x00)
    writeCammand(0x11)# sleep out
    time.sleep(0.01)
    writeCammand(0x29)# display ON
    time.sleep(0.01)
    writeCammand(0x2C)# memory write
    time.sleep(0.01)

    GPIO.output(CS,GPIO.HIGH)# inactive



LCD_init()

GPIO.output(CS,GPIO.LOW)# active
for i in range(255):
    writeCammand(0x28)
    time.sleep(1)
    writeCammand(0x29)
    time.sleep(1)

GPIO.output(CS,GPIO.HIGH)# inactive