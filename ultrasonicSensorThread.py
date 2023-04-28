import time
from ultrasonicSensor import UltrasonicSensor
from threading import Thread
from circularFifoQueue import CircularFifoQueue

class UltrasonicSensorThread(Thread):
    
    """This class creates a thread that constantly checks an UltrasonicSensor object for its distance to a (physical) object right in front of it. (The UltrasonicSensor on its own only provides a method to check the distance at one point in time.)
    
    Thus, the class will monitor to detect when the user has hovered continuously close enough to the sensor (default is 10 cm) and for a long enough duration (default is 1 second) to count as a "virtual button press."
    
    In practice, the getDistance() method of the sensor object can sometimes be inaccurate (for example, if user's hand is 8 cm away from sensor, but is wiggling a little bit, the distance returned may be inconsistent, and may be much higher than 8 cm). Therefore, after experimentation, this UltraSensorThread class will constantly check and keep track of a number of recent samples (QUEUE_CAPACITY variable below) of distances to an opposite object, storing them into a FIFO queue. If among those recent distance samples, a large enough portion of the those samples (for example, 70% as specified in the CLOSE_DISTANCE_RATE_THRESHOLD) is actually closer than the distance threshold, then that means the user has started hovering over the sensor.
    
    The distance threshold for an object to be considered "close enough" to the sensor is specified in the self.distanceThreshold variable.
    
    The self.hoverThreshold specifies for how long user's hand has to be close to the sensor to count as a "press."
    
    The self.onSensorActivatedEvent is an EventObject variable that holds the threading.Event flag that will be set to True when the user has hovered close enough for long enough. That EventObject will also hold a function to be executed (that logic is handled by the EventListener class).


    """
    
    QUEUE_CAPACITY = 16
    CLOSE_DISTANCE_RATE_THRESHOLD = 0.7
    
    def __init__(self, trigPin, echoPin, ledPin, distanceThreshold=10, hoverThreshold=1, name=""):
        Thread.__init__(self)
        
        self.ultrasonicSensor = UltrasonicSensor(trigPin, echoPin, ledPin)
        self.distanceThreshold = distanceThreshold # user has to hover how close to "press the virtual button" (in cm)?
        self.hoverThreshold = hoverThreshold # user has to hover for how long to "press" (in seconds)?
        self.name = name
        self.onSensorActivatedEvent = None
        
        self.continueRunning = True
        self.currentState = UltrasonicSensor.INACTIVE_STATE
        
        # some variables to help the main methods
        self.countInSequence = 0
        self.countCloseDistance = 0
        self.lastInactiveToActive = 0
        self.distanceQueue = CircularFifoQueue(UltrasonicSensorThread.QUEUE_CAPACITY)
    
    def updateState(self):
        """This method updates the self.currentState variable to indicates whether there's an object right in front of the sensor within the close enough distance or not. To increase the stability and accuracy of the method, a FIFO queue is used to keep track of a number of most recent distance samples, instead of measuring the distance only once (see explanation in the class documentation above).

        Returns:
            Besides updating self.currentState, the method also returns the value of that current state
        """
        
        # sample the distance from the sensor to an opposite object at one moment in time
        newDistance = self.ultrasonicSensor.getDistance()
        
        # save that new distance sample into a queue (which is the self.distanceQueue variable)
        # if the queue is not yet filled, then just add to queue
        if self.distanceQueue.queueSize < UltrasonicSensorThread.QUEUE_CAPACITY:
            self.countInSequence += 1
            self.distanceQueue.enqueue(newDistance)
        
        # if the queue is already full, then remove the oldest distance first before adding the most recent sample (FIFO)
        else:
            removed = self.distanceQueue.dequeue()
            if removed < self.distanceThreshold:
                self.countCloseDistance -= 1
            self.distanceQueue.enqueue(newDistance)
        
        # update the count of distances that are less than self.distanceThreshold
        if newDistance < self.distanceThreshold:
                self.countCloseDistance += 1
        
        # then compare the rate of "close enough" distance in the queue to the threshold rate (default 70%). If smaller than threshold rate, then the state of the sensor is ACTIVE_STATE
        closeDistanceRate = self.countCloseDistance / self.countInSequence
        self.currentState = UltrasonicSensor.ACTIVE_STATE if closeDistanceRate > UltrasonicSensorThread.CLOSE_DISTANCE_RATE_THRESHOLD else UltrasonicSensor.INACTIVE_STATE
        
        # switch on / off the LED light accordingly
        if self.currentState:
            self.ultrasonicSensor.turnOnLed()
        else:
            self.ultrasonicSensor.turnOffLed()
        return self.currentState
                
        
    def run(self):
        try:
            while self.continueRunning:
                previousState = self.currentState
                # update the sensor's current state, if the state changes, then update the appropriate time stamp
                if self.updateState() != previousState:
                    if self.currentState == UltrasonicSensor.ACTIVE_STATE:
                        self.onInactiveToActive()
                    else:
                        self.onActiveToInactive()
                
                # if the state doesn't change, and is continuously staying activated, then compute the time since the last time that the state changed from INACTIVE to ACTIVE. If that time is longer than self.hoverThreshold, then that is considered a "button press"
                else:
                    if self.currentState == UltrasonicSensor.ACTIVE_STATE:
                        if (time.time() - self.lastActivatedMoment > self.hoverThreshold):
                            
                            # if self.currentState is indeed ACTIVE for longer than self.hoverThreshold, then mark the current point in time in order to determine possible consecutive "button presses." (In other words, if the user keeps their hand constantly close to the sensor, then, and self.hoverThreshold is current set to 1 second, then every consecutive 1-second interval will be counted as consecutive "button press")
                            self.lastActivatedMoment = time.time()
                            
                            # invoke the method to handle the case when a "button press" has occurred
                            self.onSensorActivated()
                            
                            # empty the distance queue so that new distance samples won't be affected by distance samples from the previous "button press"
                            self._resetDistanceQueue()
        except Exception as e:
            print(e)
         
    def onInactiveToActive(self):
        self.lastInactiveToActive = time.time()
        self.lastActivatedMoment = self.lastInactiveToActive
    
    def onActiveToInactive(self):
        pass
    
    def onSensorActivated(self):
        if self.onSensorActivatedEvent!=None:
            msg = f"{self.name} activated"
            self.onSensorActivatedEvent.message = msg
            self.onSensorActivatedEvent.event.set()
        print("INSIDE SENSOR THREAD", self.name,"button pressed",(time.time()))

               
    def stop(self):
        self.continueRunning = False
        
    def _resetDistanceQueue(self):
        while self.distanceQueue.queueSize > 0:
            self.distanceQueue.dequeue()
            self.countCloseDistance = 0
            self.countInSequence = 0
        
# ust = UltrasonicSensorThread(trigPin=21, echoPin=20, ledPin=14)
# ust.start()