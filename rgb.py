import RPi.GPIO as GPIO
from flask import Flask
app = Flask(__name__)

class LED(object):
    R_PIN = 33
    G_PIN = 35
    B_PIN = 37
    RED_COLOR = 0xFF0000
    GREEN_COLOR = 0x00FF00
    PINS = {'pin_R': 33, 'pin_G': 35, 'pin_B': 37}

    def set_off(self):
        for i in pins:
            GPIO.output(pins[i], GPIO.HIGH)  # Turn off all leds

    def set_red(self):
        self._setColor(self.RED_COLOR)

    def set_green(self):
        self._setColor(self.GREEN_COLOR)

    def destroy(self):
        try:
            self.p_R.stop()
            self.p_G.stop()
            self.p_B.stop()
            self.set_off()
            GPIO.cleanup()
        except Exception:
            pass

    def setup(self):
        self.destroy()
        GPIO.setmode(GPIO.BOARD)  # Numbers GPIOs by physical location
        for i in self.PINS:
            GPIO.setup(self.PINS[i], GPIO.OUT)  # Set pins' mode is output
            GPIO.output(self.PINS[i], GPIO.HIGH)  # Set pins to high(+3.3V) to off led
        self.p_R = GPIO.PWM(self.PINS['pin_R'], 2000)  # set Frequece to 2KHz
        self.p_G = GPIO.PWM(self.PINS['pin_G'], 1999)
        self.p_B = GPIO.PWM(self.PINS['pin_B'], 5000)
        self.p_R.start(100)  # Initial duty Cycle = 0(leds off)
        self.p_G.start(100)
        self.p_B.start(100)

    def _map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def _setColor(self, col):  # For example : col = 0x112233
        R_val = (col & 0xff0000) >> 16
        G_val = (col & 0x00ff00) >> 8
        B_val = (col & 0x0000ff) >> 0
        R_val = self._map(R_val, 0, 255, 0, 100)
        G_val = self._map(G_val, 0, 255, 0, 100)
        B_val = self._map(B_val, 0, 255, 0, 100)
        self.p_R.ChangeDutyCycle(100 - R_val)  # Change duty cycle
        self.p_G.ChangeDutyCycle(100 - G_val)
        self.p_B.ChangeDutyCycle(100 - B_val)


led = LED()


@app.route("/led/<action>", methods=['GET'])
def action(action):
    success = True
    try:
        if action == "set_red":
            led.set_red()
        elif action == "set_green":
            led.set_green()
        elif action == "set_off":
            led.set_off()
        elif action == "destroy":
            led.destroy()
        elif action == "setup":
            led.setup()
        else:
            success = False
    except Exception, e:
        success = False

    return 'success', 200 if success else 'fail', 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
