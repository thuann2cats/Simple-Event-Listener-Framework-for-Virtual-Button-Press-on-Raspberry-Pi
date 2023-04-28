import time
import RPi.GPIO as GPIO

class LDRSensor:
    """This class will represent an Light-Dependent Resistor that is connected to the Raspberry Pi according to the diagram.
    
    This object can tell whether the room is bright (has the light on) or dark (light off). The principle is that the LDR's resistance depends on the intensity of light that hits it. Therefore, one end of the LDR is initially set to LOW voltage. Eventually the current will flow from the HIGH voltage end to the LOW voltage end, making the other end become HIGH. The time it takes for that LOW-voltage pin to become HIGH will be a proxy for the amount of resistance in the LDR, and thus for the current light intensity.
    """

    LIGHT_ON_STATE = 1
    LIGHT_OFF_STATE = 0
    
    def __init__(self, LDRPin, lightOnThreshold=300000):
        self.LDRPin = LDRPin    # need to pass in the GPIO pin number used to connect to the LDR sensor
        self.lightOnThreshold = lightOnThreshold
        self.currentState = self.LIGHT_OFF_STATE
      
        GPIO.setmode(GPIO.BCM)
        
    def getReading(self):
        """This method sets the 'LDRPin' pin on the Raspberry Pi to GPIO.LOW voltage, then do a while loop until that pin becomes GPIO.HIGH. A count within the loop will be a measure of how long it takes for that pin to go from GPIO.LOW to GPIO.HIGH.

        Returns:
            an integer: the brighter the room is, the smaller this integer will be
        """
        NUM_OF_SAMPLES = 1 # number of times the method will sample light intensity
        SLEEP_TIME = 0.01 
        
        totalReading = 0
        for i in range(NUM_OF_SAMPLES):
            reading = 0
            GPIO.setup(self.LDRPin, GPIO.OUT)
            GPIO.output(self.LDRPin, GPIO.LOW)
            time.sleep(SLEEP_TIME) # so that the capacitor of the LDR circuit to discharge after the GPIO pin is set to low
            GPIO.setup(self.LDRPin, GPIO.IN)
            while GPIO.input(self.LDRPin)==GPIO.LOW:
                reading += 1
                if reading > self.lightOnThreshold:
                    break
            totalReading += reading
            # print(totalReading)
        return int(totalReading / NUM_OF_SAMPLES)
    
    def isLightOn(self):
        if self.getReading() < self.lightOnThreshold:
            return True
        else:
            return False
        
    def isLightOff(self):
        return not self.isLightOn()
            
    