from threading import Thread
import time
from LDRSensor import LDRSensor
import traceback

class LDRSensorThread(Thread):
    """This class creates a thread to constantly check a LDR sensor and to detect when the light is switched on and switched off. (The LDRSensor class on its own only provides the method to check for light-on/light-off state at one point in time only.)
    
    An object of this type has a self.ldrSensor instance variable to represents a specific LDR sensor.
    
    The instance variables self.lightSwitchedOnEvent and self.lightSwitchedOffEvent are of the EventObject class (defined also in another file in this library). This EventObject class represents an event handler, which contains a threading.Event flag and a function. When the threading.Event flag is set to True, that function will be executed (due to the logic in the EventListener class which is also defined in another file in this library).
    
    This LDRSensorThread class keeps track of how long the light has been on / off when it is switched off / on. This way, we can set a threshold - meaning only after a certain period will the self.lightSwitchedOnEvent and self.lightSwitchedOffEvent variables be updated. The reason is that we do not want to toggle the self.lightSwitchedOnEvent and self.lightSwitchedOffEvent variables when a user merely turns on the light and off again too quickly.
    
    
    """
    def __init__(self, LDRPin, lightOnThreshold=300000, darkThreshold=600):
        Thread.__init__(self)
        self.ldrSensor = LDRSensor(LDRPin, lightOnThreshold)
        self.currentState = LDRSensor.LIGHT_OFF_STATE if self.ldrSensor.isLightOff() else LDRSensor.LIGHT_ON_STATE
        if self.currentState == LDRSensor.LIGHT_ON_STATE:
            self.lastOffToOn = time.time()
        else:
            self.lastOnToOff = time.time()
        
        self.continueRunning = True
        self.lightSwitchedOnEvent = None
        self.lightSwitchedOffEvent = None
        self.DARK_THRESHOLD = darkThreshold
        
    def stop(self): # provide a method to stop this thread
        self.continueRunning = False

    def updateLightState(self):
        """Update the self.currentState variable to indicate whether the room was bright or dark, relying on the function of the LDRSensor class that serves this objective.

        Returns:
            Besides updating self.currentState, the method also returns the value of that current state
        """
        self.currentState = LDRSensor.LIGHT_ON_STATE if self.ldrSensor.isLightOn() else LDRSensor.LIGHT_OFF_STATE
        return self.currentState

    def onLightSwitchedOn(self):
        # print("here here light on")
        
        
        # whenever the light is switched on, update the time stamp of the last-switched-on moment
        self.lastOffToOn = time.time()
        
        # calculate how long the room has been dark, by comparing current time with last-switched-off moment
        offDuration = time.time() - self.lastOnToOff
        
        if offDuration >= self.DARK_THRESHOLD:
            
            # if self.lightSwitchedOnEvent is not None, meaning there's an EventObject object that is attached to this event at this specific LDR sensor
            if self.lightSwitchedOnEvent!=None:
                
                # update the message field of that EventObject, in case the event handler function needs this message
                self.lightSwitchedOnEvent.message = f"Light switched ON after {str(round(offDuration, 1))} seconds of being OFF!"
                
                # set the flag within the event field to True, so that an object of the EventListener class can execute the event handler function
                self.lightSwitchedOnEvent.event.set()

        
    def onLightSwitchedOff(self):
        """Please see comments and explanation in the similar onLightSwitchedOn function above.
        """
        # print("here here light OFF")
        self.lastOnToOff = time.time()
        onDuration = time.time() - self.lastOffToOn
        
        if self.lightSwitchedOffEvent!=None:
            self.lightSwitchedOffEvent.message = f"Light switched OFF after {str(round(onDuration, 1))} seconds of being ON!"
            self.lightSwitchedOffEvent.event.set()

        
    def run(self):
        """This method starts the thread that would constantly update the self.currentState variable. This variable indicates whether the room is bright or dark. Upon detecting that self.currentState has changed. This method invokes the appropriate methods.
        """
        try:
            while self.continueRunning:
                time.sleep(0.001)
                previousState = self.currentState
                # print(previousState)
                if self.updateLightState() != previousState:
                    if self.currentState == LDRSensor.LIGHT_ON_STATE:
                        self.onLightSwitchedOn()
                    else:
                        self.onLightSwitchedOff()
        except Exception as e:
            traceback.print_exc()
            print(e)
        
