from ultrasonicSensorThread import UltrasonicSensorThread
from LDRSensorThread import LDRSensorThread
from eventListener import EventListener, EventObject
import RPi.GPIO as GPIO
from speaker import Speaker
from threading import Event
from getWeather import WeatherForecast
from getNews import NewsFeed
import time
from recordReminder import Reminder

LOCATION = "New York"
TOPIC = "World"

# instantiate threads that represent 3 ultrasonic sensors and 1 LDR sensor
us1 = UltrasonicSensorThread(trigPin=21, echoPin=20, ledPin=14, name="Sensor #1")
us2 = UltrasonicSensorThread(trigPin=9, echoPin=10, ledPin=15, name="Sensor #2")
us3 = UltrasonicSensorThread(trigPin=19, echoPin=13, ledPin=18, name="Sensor #3")

ldr1 = LDRSensorThread(LDRPin=23, darkThreshold=10) # the sensor will consider the user to be "waking up" if the light is switched on after 10 seconds of darkness (just for illustration purpose)

# instantiate an EventListener object (which is actually a thread) that coordinates the EventObjects above
cancelFlag = Event()
listener = EventListener(cancelFlag)
 
# instantiate EventObject variables, and pass those EventObjects into the appropriate event fields within the objects that represent the sensor threads
ldr1OnEventObject = EventObject()
ldr1.lightSwitchedOnEvent = ldr1OnEventObject

# ldr1OffEventObject = EventObject()
# ldr1.lightSwitchedOffEvent = ldr1OffEventObject

sensor1ActivatedEventObject = EventObject()
sensor1ActivatedEventObject.allowConcurrent = True
us1.onSensorActivatedEvent = sensor1ActivatedEventObject

sensor2ActivatedEventObject = EventObject()
us2.onSensorActivatedEvent = sensor2ActivatedEventObject

sensor3ActivatedEventObject = EventObject()
us3.onSensorActivatedEvent = sensor3ActivatedEventObject


# define the functions to included within the EventObjects. These functions need to take in 'cancelFlag' as the first argument, which should be checked periodically to see if the function is being asked to complete executing ASAP
# def LDROnHandler(cancelFlag, message):
#     print(message)
#     Speaker.speak(cancelFlag, message) # in this example, these functions simply speak the sentences specified in the 'message' parameter
    
# def LDROffHandler(cancelFlag, message):
#     print(message)
#     Speaker.speak(cancelFlag, message)

def recordSensorActivated(cancelFlag, message):
    Speaker.speak(Event(), "Please start recording (hover CANCEL to end recording)...")
    # time.sleep(1.5)
    rm = Reminder(fileName="memo.wav", cancelFlag=cancelFlag)
    rm.record()
    
def readReminder(cancelFlag, message):
    # pass
    Speaker.playFile(cancelFlag, "memo.wav")

def userWakesUp(cancelFlag, message):
    Speaker.speak(cancelFlag, "Hello! It seems that you have just woken up!")
    
    if cancelFlag.is_set():
        return
    readWeatherAndNews(cancelFlag, message)
    
def sensor1ActivatedHandler(cancelFlag, message):
    cancelFlag.set()
    # Speaker.speak(Event(), "Cancelled")

def readWeatherAndNews(cancelFlag, message):
    
    Speaker.speak(cancelFlag, "Here are your personal reminder - weather and news! Hover CANCEL to skip to next")
    
    if cancelFlag.is_set()==False:
        readReminder(cancelFlag, message)
    cancelFlag.clear()
    
    # if cancelFlag.is_set():
    #     return
    
    
    Speaker.speak(cancelFlag, "Here's the weather")
    
    if cancelFlag.is_set()==False:
    
        wf = WeatherForecast(location=LOCATION)
        forecastString = wf.getWeather()
        Speaker.speak(cancelFlag, forecastString)
    
    cancelFlag.clear()
    
    
    Speaker.speak(cancelFlag, "Here are the latest headlines and sources... in just a moment")

    if cancelFlag.is_set()==False:
        
        nf = NewsFeed(topic=TOPIC, location=LOCATION)
        nf.update()
        newsSummary = nf.getNewsSummary()
        Speaker.speak(cancelFlag, newsSummary)
        
    
    

    
    
    
    
# "attach" the EventObjects to 'listener,' also passing in the corresponding functions to be executed when the appropriate EventObjects are updated by the sensor threads
listener.attachEventHandler(ldr1OnEventObject, userWakesUp)
# listener.attachEventHandler(ldr1OffEventObject, LDROffHandler)
listener.attachEventHandler(sensor1ActivatedEventObject, sensor1ActivatedHandler)
listener.attachEventHandler(sensor2ActivatedEventObject, readWeatherAndNews)
listener.attachEventHandler(sensor3ActivatedEventObject, recordSensorActivated)

# start the threads
listener.start()
ldr1.start()
us1.start()
us2.start()
us3.start()
