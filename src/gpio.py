import RPi.GPIO as GPIO

class PWM:
    resistPin = 23				        # PWM pin connected to LED
    fanPin = 24
    PWMRANGE = [40, 100]
    intensity = 0
    resist_pwm = None
    fan_pwm = None
    def __init__(self):
        GPIO.setwarnings(False)			# disable warnings
        GPIO.setmode(GPIO.BCM)		    # set pin numbering system
        GPIO.setup(self.resistPin,GPIO.OUT)
        GPIO.setup(self.fanPin,GPIO.OUT)
        self.resist_pwm = GPIO.PWM(self.resistPin,1000)		# create PWM instance with frequency
        self.fan_pwm = GPIO.PWM(self.fanPin,1000)		    # create PWM instance with frequency
        self.resist_pwm.ChangeDutyCycle(0)
        self.fan_pwm.ChangeDutyCycle(0)

    def __le__(self, intensity):
        if intensity < 0:
            intensity = -intensity
            if intensity == self.intensity:
                return intensity
            self.intensity = min(self.PWMRANGE[1], intensity)
            self.intensity = max(self.PWMRANGE[0], intensity)
            self.resist_pwm.ChangeDutyCycle(0)
            self.fan_pwm.ChangeDutyCycle(self.intensity)
            return self.intensity
        else:
            if intensity == self.intensity:
                return intensity
            self.intensity = min(self.PWMRANGE[1], intensity)
            self.resist_pwm.ChangeDutyCycle(intensity)
            self.fan_pwm.ChangeDutyCycle(0)
        return self.intensity