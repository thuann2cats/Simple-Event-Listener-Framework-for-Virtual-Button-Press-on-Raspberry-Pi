from ultrasonicSensorThread import UltrasonicSensorThread
from LDRSensorThread import LDRSensorThread
from eventListener import EventListener, EventObject
import RPi.GPIO as GPIO
from speaker import Speaker

# instantiate threads that represent 3 ultrasonic sensors and 1 LDR sensor
us1 = UltrasonicSensorThread(trigPin=21, echoPin=20, ledPin=14, name="Sensor #1")
us2 = UltrasonicSensorThread(trigPin=9, echoPin=10, ledPin=15, name="Sensor #2")
us3 = UltrasonicSensorThread(trigPin=19, echoPin=13, ledPin=18, name="Sensor #3")
ldr1 = LDRSensorThread(LDRPin=23)

 
# instantiate EventObject variables, and pass those EventObjects into the appropriate event fields within the objects that represent the sensor threads
ldr1OnEventObject = EventObject()
ldr1.lightSwitchedOnEvent = ldr1OnEventObject

ldr1OffEventObject = EventObject()
ldr1.lightSwitchedOffEvent = ldr1OffEventObject

sensor1ActivatedEventObject = EventObject()
us1.onSensorActivatedEvent = sensor1ActivatedEventObject

sensor2ActivatedEventObject = EventObject()
us2.onSensorActivatedEvent = sensor2ActivatedEventObject

sensor3ActivatedEventObject = EventObject()
us3.onSensorActivatedEvent = sensor3ActivatedEventObject


# define the functions to included within the EventObjects. These functions need to take in 'cancelFlag' as the first argument, which should be checked periodically to see if the function is being asked to complete executing ASAP
def LDROnHandler(cancelFlag, message):
    print(message)
    Speaker.speak(cancelFlag, message) # in this example, these functions simply speak the sentences specified in the 'message' parameter
    
def LDROffHandler(cancelFlag, message):
    print(message)
    Speaker.speak(cancelFlag, message)
    
def sensor1ActivatedHandler(cancelFlag, message):
    Speaker.speak(cancelFlag, message)
    print(message)

def sensor2ActivatedHandler(cancelFlag, message):
    Speaker.speak(cancelFlag, message)
    print(message)

def sensor3ActivatedHandler(cancelFlag, message):
    Speaker.speak(cancelFlag, message)
    print(message)
    
    
# instantiate an EventListener object (which is actually a thread) that coordinates the EventObjects above
listener = EventListener()
    
# "attach" the EventObjects to 'listener,' also passing in the corresponding functions to be executed when the appropriate EventObjects are updated by the sensor threads
listener.attachEventHandler(ldr1OnEventObject, LDROnHandler)
listener.attachEventHandler(ldr1OffEventObject, LDROffHandler)
listener.attachEventHandler(sensor1ActivatedEventObject, sensor1ActivatedHandler)
listener.attachEventHandler(sensor2ActivatedEventObject, sensor2ActivatedHandler)
listener.attachEventHandler(sensor3ActivatedEventObject, sensor3ActivatedHandler)

# start the threads
listener.start()
ldr1.start()
us1.start()
us2.start()
us3.start()
