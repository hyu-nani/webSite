
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

#command list
SoftwareReset = 0x01
ReadDisplayIdentificationInformatioin = 0x04
ReadDisplayStatus = 0x09
ReadDisplayPowerMode = 0x0A
ReadDisplay_MADCTL = 0x0B
ReadDisplayPixelFormat = 0x0C
ReadDisplayImageFormat = 0x0D
ReadDisplaySignalmode = 0x0E
ReadDisplaySelfDiagnosticResult = 0x0F
EnterSleepMode = 0x10
Sleep_OUT = 0x11
PartialMode_ON = 0x12
NormalDisplayMode = 0x13
DisplayInversion_OFF = 0x20
DisplayInversion_ON = 0x21
GammaSet = 0x26
Display_OFF = 0x28
Display_ON = 0x29
ColumnAddressSet = 0x2A
PageAddressSet = 0x2B
MemoryWrite = 0x2C
ColorSet = 0x2D
MemoryRead = 0x2E
PartialArea = 0x30
VerticalScrollingDefinition = 0x33
TearingEffectLine_OFF = 0x34
TearingEffectLine_ON = 0x35
MemoryAccessControl = 0x36
VerticalScrollingStartAddress = 0x37
IdleMode_OFF = 0x38
IdleMode_ON = 0x39
PixelFormatSet = 0x3A
WriteMemoryContinue = 0x3C
ReadMemoryContinue = 0x3E
SetTearScanline = 0x44
GetScanline = 0x45
WriteDisplayBrightness = 0x51

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

def commandSet(bit):
    GPIO.output(RS,GPIO.LOW)
    GPIO.output(RD,GPIO.HIGH)
    GPIO.output(WR,GPIO.LOW)
    LCDdata(bit)
    GPIO.output(WR,GPIO.HIGH)
    GPIO.output(RS,GPIO.HIGH)

def LCD_init():
    GPIO.output(CS,GPIO.LOW)#active
    commandSet(SoftwareReset)
    for i in range(255):
        commandSet(WriteDisplayBrightness)
        GPIO.output(RD,GPIO.HIGH)
        GPIO.output(WR,GPIO.LOW)
        LCDdata(i)
        GPIO.output(WR,GPIO.HIGH)
        sleep(0.5)




TFTgpio_set()
LCD_init()