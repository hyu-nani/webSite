
import RPi.GPIO as GPIO
import time
import os

'''
하드웨어 핀 연결도 GPIO핀
'''
dataPin = [19, 13, 6, 5, 1, 7, 8, 25] # D0~D7
RS = 20 #D/C
CS = 21
RD = 26
WR = 16
RES = 12 #reset
BLK = 2

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
for i in range(8):
    GPIO.setup(dataPin[i], GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(RS, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(CS, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(RD, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(WR, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(RES, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(BLK, GPIO.OUT, initial=GPIO.HIGH)

def LCDdata(bit):
    for i in range(8):
        GPIO.output(dataPin[i],((bit >> i) & 0x01))

def writeCammand(bit):
    GPIO.output(RS,GPIO.LOW)
    GPIO.output(WR,GPIO.LOW)
    LCDdata(bit)
    GPIO.output(WR,GPIO.HIGH)

def writeData(bit):
    GPIO.output(RS,GPIO.HIGH)
    GPIO.output(WR,GPIO.LOW)
    LCDdata(bit)
    GPIO.output(WR,GPIO.HIGH)

def LCD_init():
    GPIO.output(BLK,0)
    GPIO.output(CS,GPIO.LOW)# active
    # start inittial code
    GPIO.output(RES,GPIO.HIGH)
    time.sleep(0.001)
    GPIO.output(RES,GPIO.LOW)
    time.sleep(0.01)
    GPIO.output(RES,GPIO.HIGH)
    time.sleep(0.12)
    

    writeCammand(0x28) #display OFF
    writeCammand(0x11)#sleep out
    writeData(0x00)
    writeCammand(0xCB)#Power Control A
    writeData(0x39)#always 0x39     
    writeData(0x2C) #always 0x2C    
    writeData(0x00) #always 0x  
    writeData(0x34) #Vcore = 1.6V
    writeData(0x02) #DDVDH = 5.6V
    writeCammand(0xCF) #Power Control B
    writeData(0x00) #always 0x
    writeData(0x81) #PCEQ off
    writeData(0x30) #ESD protection
    writeCammand(0xE8) #Driver timing control A
    writeData(0x85) #non‐overlap
    writeData(0x01) #EQ timing
    writeData(0x79) #Pre‐charge timing
    writeCammand(0xEA) #Driver timing control B
    writeData(0x00) #Gate driver timing
    writeData(0x00) #always 0x
    writeCammand(0xED) #Power‐On sequence control
    writeData(0x64) #soft start
    writeData(0x03) #power on sequence
    writeData(0x12) #power on sequence
    writeData(0x81) #DDVDH enhance on
    writeCammand(0xF7) #Pump ratio control
    writeData(0x20) #DDVDH=2xVCI
    writeCammand(0xC0) #power control 1
    writeData(0x26)
    writeData(0x04) #second parameter for ILI9340 (ignored by ILI9341)
    writeCammand(0xC1) #power control 2
    writeData(0x11)
    writeCammand(0xC5) #VCOM control 1
    writeData(0x35)
    writeData(0x3E)
    writeCammand(0xC7) #VCOM control 2
    writeData(0xBE)
    writeCammand(0x36) #memory access control = BGR
    writeData(0x88)
    writeCammand(0xB1) #frame rate control
    writeData(0x00)
    writeData(0x10)
    writeCammand(0xB6) #display function control
    writeData(0x0A)
    writeData(0xA2)
    writeCammand(0x3A) #pixel format = 16 bit per pixel
    writeData(0x55)
    writeCammand(0xF2) #3G Gamma control
    writeData(0x02) #off
    writeCammand(0x26) #Gamma curve 3
    writeData(0x01)
    writeCammand(0x2A) #column address set
    writeData(0x00)
    writeData(0x00) #start 0x00
    writeData(0x00)
    writeData(0xEF) #end 0xEF
    writeCammand(0x2B) #page address set
    writeData(0x00)
    writeData(0x00) #start 0x00
    writeData(0x01)
    writeData(0x3F) #end 0x013F
    
    writeCammand(0x29) #display ON

    GPIO.output(CS,GPIO.HIGH)# inactive
    GPIO.output(BLK,1)

def LCD_AddressSet(x1,y1,x2,y2):
    writeCammand(0x2A)
    writeData(x1)
    writeData(x2)
    writeCammand(0x2B)
    writeData(y1)
    writeData(y2)

LCD_init()

GPIO.output(CS,GPIO.LOW)# active

LCD_AddressSet(0,0,100,100)
writeCammand(0x2C)
for i in range(100):
    for j in range(100):
        writeData(0x2A)
for i in range(100):
    writeCammand(0x28)
    time.sleep(1)
    writeCammand(0x29)
    time.sleep(1)
time.sleep(1)

GPIO.output(CS,GPIO.HIGH)# inactive