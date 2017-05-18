# !/usr/bin/env python
import RPi.GPIO as GPIO
import time


class LED(object):
    R_PIN = 33
    G_PIN = 35
    B_PIN = 37
    RED_COLOR = 0xFF0000
    GREEN_COLOR = 0x00FF00
    
    def __init__(self):
    
        self._setup(self.R_PIN, self.G_PIN, self.B_PIN)
    def setOff():
        for i in pins:
            GPIO.output(pins[i], GPIO.HIGH)    # Turn off all leds
    
    def setRed(self):
        self._setColor(self.RED_COLOR)
    def setGreen(self):
        self._setColor(self.GREEN_COLOR)
    def destroy(self):
        p_R.stop()
        p_G.stop()
        p_B.stop()
        self.setOff()
        GPIO.cleanup()
    
    def _setup(self, Rpin, Gpin, Bpin):
        global pins
        global p_R, p_G, p_B
        pins = {'pin_R': Rpin, 'pin_G': Gpin, 'pin_B': Bpin}
        GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
        for i in pins:
            GPIO.setup(pins[i], GPIO.OUT)   # Set pins' mode is output
            GPIO.output(pins[i], GPIO.HIGH) # Set pins to high(+3.3V) to off led
        
        p_R = GPIO.PWM(pins['pin_R'], 2000)  # set Frequece to 2KHz
        p_G = GPIO.PWM(pins['pin_G'], 1999)
        p_B = GPIO.PWM(pins['pin_B'], 5000)
        
        p_R.start(100)      # Initial duty Cycle = 0(leds off)
        p_G.start(100)
        p_B.start(100)
    
    def _map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def _setColor(self, col):   # For example : col = 0x112233
        R_val = (col & 0xff0000) >> 16
        G_val = (col & 0x00ff00) >> 8
        B_val = (col & 0x0000ff) >> 0
    
        R_val = self._map(R_val, 0, 255, 0, 100)
        G_val = self._map(G_val, 0, 255, 0, 100)
        B_val = self._map(B_val, 0, 255, 0, 100)
        
        p_R.ChangeDutyCycle(100-R_val)     # Change duty cycle
        p_G.ChangeDutyCycle(100-G_val)
        p_B.ChangeDutyCycle(100-B_val)