import threading
import RPi.GPIO as GPIO
import time

class UltrasonicSensor:
    """This class represents an ultrasonic sensor HC-SR04 that is connected to the Raspberry Pi according to the diagram.
    
    Once the HC-SR04 sensor has been connected, the GPIO pins that connect to the TRIG and ECHO pins of the sensor need to be passed into an object of this class and will be kept as the instance variables self.trigPin and self.echoPin.
    
    The class can measure the distance from the sensor to an object directly in front of it. The principle is that we set the TRIG pin to HIGH voltage for 10 microseconds. Then one part of the sensor will emit sound wave that will get to the object and bounce back to the other part of the sensor. Then the ECHO pin of the sensor will be HIGH voltage. The class will detect and measure how long that HIGH pulse at the ECHO pin is, and then compute the distance based on that.
    
    In addition, along with each HC-SR04 sensor, there should be an LED light connected to the Raspberry Pi. That LED will be controlled by this class, and will be on when a user hovers their hand over the sensor.
    
    Returns:
        _type_: _description_
    """
    ACTIVE_STATE = 1
    INACTIVE_STATE = 0
    
    def __init__(self, trigPin, echoPin, ledPin):
        self.trigPin = trigPin
        self.echoPin = echoPin
        self.ledPin = ledPin
        
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.ledPin, GPIO.OUT)
        GPIO.setup(self.trigPin, GPIO.OUT)
        GPIO.setup(self.echoPin, GPIO.IN)
        
    def turnOnLed(self):
        GPIO.output(self.ledPin, True)
        
    def turnOffLed(self):
        GPIO.output(self.ledPin, False)
        
    def getDistance(self):
        """Allows for the option of calling the sampleOneDistance() method multiple times in order to measure the distance to the opposite object more accurately
        
        Returns: an integer - the distance in centimeters
        
        """
        NUMBER_OF_SAMPLES = 1
        distanceArray = []
        
        # sample the distance from the sensor to opposite objects multiple times, store into the distanceArray
        for i in range(NUMBER_OF_SAMPLES):
            distanceArray.append(self.sampleOneDistance())
            
        # get the median of the distanceArray
        distanceArray.sort()
        if NUMBER_OF_SAMPLES % 2 == 1:
            medianIndex1 = NUMBER_OF_SAMPLES // 2
            medianIndex2 = medianIndex1
        else:
            medianIndex1 = NUMBER_OF_SAMPLES // 2 - 1
            medianIndex2 = medianIndex1 + 1
        median = (distanceArray[medianIndex1] + distanceArray[medianIndex2]) / 2

        return median
        
                     
    def sampleOneDistance(self):
        """This function sends a 10 microsecond pulse of HIGH voltage to the TRIG pin of the ultrasonic sensor. That will make the sensor emit sound wave. When the sound wave bounces back from an object, the ECHO pin will become HIGH for a short duration. That duration will help us compute the distance to that object.

        Returns:
            int: the distance to that object in centimeters
        """
        TIMEOUT_THRESHOLD = 0.5

        INITIAL_WAIT_TIME = 0.01
        time.sleep(INITIAL_WAIT_TIME) # for the sensor to settle
        GPIO.output(self.trigPin, GPIO.LOW)

        # send a 10 microsecond HIGH to TRIG pin of the ultrasonic sensor
        GPIO.output(self.trigPin, GPIO.HIGH)
        time.sleep(0.000010)
        GPIO.output(self.trigPin, GPIO.LOW)
        
        # measure the duration that the ECHO pin is activated (in seconds)
        startLoopTime = time.time()
        while GPIO.input(self.echoPin)==0:
            if time.time() - startLoopTime > TIMEOUT_THRESHOLD:
                break
        pulseStart = time.time()  # mark the time when the ECHO pin begins to become HIGH
            
        startLoopTime = time.time()
        while GPIO.input(self.echoPin)==1:
            if time.time() - startLoopTime > TIMEOUT_THRESHOLD:
                break
        pulseEnd = time.time() # marks the time when the ECHO pin is no longer HIGH
        
        pulseDuration = pulseEnd - pulseStart

        distance = pulseDuration * 17150

        return distance
    
    def cleanUp(self):
        GPIO.cleanup()

# sensor1 = UltrasonicSensor(trigPin=21, echoPin=20, ledPin=14)
# print(sensor1.checkDistance())
