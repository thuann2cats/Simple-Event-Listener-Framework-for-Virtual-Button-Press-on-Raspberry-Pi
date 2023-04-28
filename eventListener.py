
from threading import Event
from threading import Thread
import traceback

class EventObject:
    """This class represents an event. Objects of this class have an "event" field that is a threading.Event flag that can be set to True (for example, by a thread that is running a sensor), and when that flag is set to True, the function specified by the "func" field of this object will be executed.
    
    The "message" field can also be set in order to provide further information.
    """
    def __init__(self) -> None:
        self.event = Event()
        self.message = ""
        # self.ID = 0
        self.func = None
        self.allowConcurrent = False # if this is set to False (by default), the EventListener will not execute the function associated with this event if there are other functions from other events running
        
class SubThread(Thread):
    """This class represents a sub-thread that will be started by the EventListener class when the EventListener class detected that the "event" field of an EventObject has been set to True.
    
    This sub-thread will execute the function that is specified in the "func" field of the EventObject.
    
    Python does not seem to provide a convenient way for a parent thread (EventListener) to kill a sub-thread (in this case, the SubThread object). Therefore, the EventListener object passes 2 flags (of the threading.Event type) for monitoring purpose:
    + subThreadExecutingFlag: set to True if sub-thread is still executing, and False if sub-thread is finished
    + cancelSubThreadFlag: set to True if the sub-thread should be killed.

    The event handler function (executed by SubThread) will also be passed in this cancelSubThreadFlag as an argument, and if/when this flag is True, then that function will end its task as soon as possible.
    """
    def __init__(self, subThreadExecutingFlag, cancelSubThreadFlag, func, *args):
        Thread.__init__(self)
        self.subThreadExecutingFlag = subThreadExecutingFlag
        self.cancelSubThreadFlag = cancelSubThreadFlag
        self.func = func
        self.args = args
      
        
    def run(self):
        self.func(self.cancelSubThreadFlag, *(self.args) )
        print("executing to here")
        self.subThreadExecutingFlag.clear()
        print("executing to here here")
        self.cancelSubThreadFlag.clear()
        print("executing to here here here")

        
class EventListener(Thread):
    """This class represents an "event listener" thread which will monitor and coordinate various EventObject variables that have been "registered" with it.
    
    The EventObject variable is "attached" to this EventListener object by the attachEventHandler() method, also passing in the function to be executed when that EventListener object's "event" flag is set to True. (The EventObject object should also be passed into, for example, a sensor thread so that that thread can update that EventObject's "event" flag when the sensor detects a certain event.)
    
    Upon being started, the EventListener thread will execute the run() method, which will constant loop through all EventObject's that are registered. Upon detecting that the "event" flag of an EventObject has been updated to True, then a SubThread class will be instantiated to execute the function specified in the "func" field of the EventObject.
    
    Python does not seem to provide a convenient way for a parent thread (in this case, EventListener) to kill a sub-thread. Therefore, the EventListener object passes 2 flags (of the threading.Event type) into the SubThread object for monitoring purpose:
    
    + subThreadExecutingFlag: set to True if the sub-thread is still executing, and False if sub-thread is finished. Then in the main loop, the EventListener object will check this flag and if there's a subthread running, the EventListener will temporarily ignore other events (otherwise, multiple events might execute concurrently, confusing the user)
    
    + cancelSubThreadFlag: set to True if the sub-thread should be killed.   The event handler function (executed by SubThread) will check peridically whether this flag is True, and if so, that function will end its task as soon as possible.

    """
    def __init__(self, cancelFlag): # each argument in *args is an event object
        Thread.__init__(self)
        self.eventDictionary = {} # a dictionary that holds all EventObject's
        self.nextID = 0
        self.subThreadExecutingFlag = Event()
        self.continueRunning = True
        self.subThread = None
        self.cancelSubThreadFlag = cancelFlag

            
    def attachEventHandler(self, eventObject, func):
        """This method will add "eventObject" into self.eventDictionary, as well as setting the "func" field of that EventObject to a function specified by "func" parameter.

        Returns:
            int: this method will return an ID for that EventObject within self.eventDictionary - that can be used by the programmer to update event handler function later if necessary
        """
        newEvtObject = eventObject
        newEvtObject.func = func
        self.eventDictionary[self.nextID] = newEvtObject
        self.nextID += 1
        return self.nextID - 1
    
    def updateEventHandlerById(self, id, newFunc):
        if id not in self.eventDictionary:
            raise Exception("Event ID has not been attached in the event listener.")
        else:
            self.eventDictionary[id].func = newFunc
    
    def stop(self):
        self.continueRunning = False
        
    # def clearAllEvents(self):
    #     for eventId, eventObject in self.eventDictionary.items():
    #         eventObject.event.clear()
        
    def run(self):
        try:
            while self.continueRunning:
              
                # loop through all EventObject's in self.eventDictionary  
                for eventId, eventObject in self.eventDictionary.items():
                    
                    # print("[EventListener] checking new event objects woo hoo")
                    # if found an event that has just been set to True
                    if eventObject.event.is_set():
                        
                        # check to see if there's already a sub-thread executing
                        if self.subThreadExecutingFlag.is_set()==False:
                            self.subThreadExecutingFlag.set()
                            
                            # create a SubThread to execute the function specified within the EventObject (passing in the necessary flags, as explained the class documentation above)
                            self.subThread = SubThread(self.subThreadExecutingFlag, self.cancelSubThreadFlag, eventObject.func, eventObject.message)
                            
                            print("[EventListener] found an event and EXECUTING")
                            self.subThread.start()
                            
                            print("[EventListener] completed executing that event")
                        else:
                            # otherwise, if there's already a sub-thread executing, then check if this event is allowed to run concurrently with others
                            if eventObject.allowConcurrent:
                                # then just execute the function
                                Thread(target=eventObject.func, args=[self.cancelSubThreadFlag, eventObject.message]).start()
                                print("[EventListener] executed the cancel event")
                                
                            else:
                                print("[EventListener] found an event BUT HAVE TO CLEAR")
                        
                        # print("[EventListener] clearing that event object")
                        eventObject.event.clear()
               
        except Exception as e:
            print("error printed from here")
            print(e)
            traceback.print_exc()
    

        